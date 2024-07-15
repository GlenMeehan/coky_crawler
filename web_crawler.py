import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from collections import deque
import re
from datetime import datetime
import sqlite3
import json
from connect_sql import connect_to_database
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from robots import can_fetch
from crawl_state import save_crawl_state, load_crawl_state, get_next_url_from_crawl_state
from pagerank import calculate_pagerank
from age_rating import age_rating

def check_stop_flag():
    try:
        with open('stop_flag.txt', 'r') as f:
            return f.read().strip() == '1'
    except Exception as e:
        print(f"Error reading stop flag: {e}")
        return False

def insert_into_db(cursor, url, title, content, meta_keywords, author, publish_date, headers, links, word_count, keywords, language, page_rank, backlinks, internal_links, outbound_links, ctr, last_crawled, age_rating):
    cursor.execute(
        """
        INSERT INTO web_index (
            url, title, content, meta_keywords, author, publish_date, headers, links, word_count,
            keywords, language, page_rank, backlinks, internal_links, outbound_links, ctr, last_crawled, age_rating
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (url, title, content, meta_keywords, author, publish_date, headers, links, word_count, keywords,
         language, page_rank, backlinks, internal_links, outbound_links, ctr, last_crawled, age_rating)
    )
    print(f"Successfully added to index: {url}")

def is_external_link(url, seed_url):
    return urlparse(url).netloc != urlparse(seed_url).netloc

def filter_urls(urls, crawled_urls, max_depth):
    filtered_urls = []
    for url, depth in urls:
        if url not in crawled_urls and depth <= max_depth:
            filtered_urls.append((url, depth))
    return deque(filtered_urls)

def crawl(seed_url, search_term, synonyms, max_results=None, max_depth=1):
    conn, cursor = connect_to_database()

    # Load previously saved state
    urls_to_crawl = deque(load_crawl_state(conn))
    if not urls_to_crawl:
        urls_to_crawl.append((seed_url, 0))

    user_agent = 'YourCrawlerBot/1.0'

    session = requests.Session()
    retries = Retry(total=5, backoff_factor=1, status_forcelist=[429])
    session.mount('http://', HTTPAdapter(max_retries=retries))
    session.mount('https://', HTTPAdapter(max_retries=retries))

    result_count = 0
    results = []
    links_list = []
    crawled_urls = set()

    if max_results is not None:
        max_results = int(max_results)

    try:
        while urls_to_crawl and (max_results is None or result_count < max_results):
            if check_stop_flag():
                print("Crawling stopped by user.")
                exit()  # Immediately stop the script

            current_url, depth = urls_to_crawl.popleft()
            print(f"Crawling URL: {current_url}, Depth: {depth}")

            if depth > max_depth:
                continue

            if not can_fetch(current_url, user_agent):
                print(f"Disallowed by robots.txt: {current_url}")
                continue

            try:
                response = session.get(current_url, headers={'User-Agent': user_agent})
                response.raise_for_status()
            except requests.RequestException as e:
                print(f"Exception while crawling {current_url}: {e}")
                continue

            soup = BeautifulSoup(response.content, 'html.parser')
            title = soup.title.string if soup.title else "No Title"
            page_text = soup.get_text()

            if re.search(search_term, page_text, re.IGNORECASE) or any(re.search(synonym, page_text, re.IGNORECASE) for synonym in synonyms):
                meta_keywords = ",".join([meta['content'] for meta in soup.find_all('meta', attrs={'name': 'keywords'})])
                author = ",".join([meta['content'] for meta in soup.find_all('meta', attrs={'name': 'author'})])
                publish_date = None
                headers = json.dumps({header.name: header.text.strip() for header in soup.find_all(re.compile('^h[1-6]$'))})
                links = json.dumps([link.get('href') for link in soup.find_all('a', href=True)])
                word_count = len(page_text.split())
                keywords = meta_keywords
                language = soup.find('html').get('lang') if soup.find('html') else None
                page_rank = 0  # Placeholder for page rank
                backlinks = 0  # Placeholder for backlinks
                internal_links = len([link for link in soup.find_all('a', href=True) if not is_external_link(link.get('href'), seed_url)])
                outbound_links = len([link for link in soup.find_all('a', href=True) if is_external_link(link.get('href'), seed_url)])
                ctr = 0.0  # Placeholder for click-through rate
                last_crawled = datetime.now().isoformat()
                age_rating_value = age_rating(page_text)

                try:
                    insert_into_db(cursor, current_url, title, page_text, meta_keywords, author, publish_date, headers, links, word_count, keywords, language, page_rank, backlinks, internal_links, outbound_links, ctr, last_crawled, age_rating_value)
                    conn.commit()
                    result_count += 1
                    print(f"Successfully added to index: {current_url}")
                    results.append((current_url, title))
                except Exception as e:
                    print(f"Error inserting into database: {e}")

                for link_tag in soup.find_all('a', href=True):
                    link = urljoin(current_url, link_tag['href'])
                    parsed_link = urlparse(link)
                    cleaned_link = parsed_link._replace(fragment='').geturl()
                    links_list.append((current_url, cleaned_link))
                    if cleaned_link not in crawled_urls and depth + 1 <= max_depth:
                        urls_to_crawl.append((cleaned_link, depth + 1))
                        print(f"Adding to queue: {cleaned_link} with depth {depth + 1}")

            # Save the updated state
            urls_to_crawl = filter_urls(urls_to_crawl, crawled_urls, max_depth)
            save_crawl_state(conn, urls_to_crawl)
            crawled_urls.add(current_url)

    except Exception as ex:
        print(f"Exception during crawling: {ex}")

    finally:
        # Calculate PageRank for the crawled URLs
        pages = list(crawled_urls)
        pagerank = calculate_pagerank(pages, links_list)
        for page, rank in pagerank.items():
            cursor.execute("UPDATE web_index SET page_rank = ? WHERE url = ?", (rank, page))
        conn.commit()

        cursor.close()
        conn.close()

    return results if results else None

