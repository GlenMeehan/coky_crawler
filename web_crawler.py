import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from collections import deque
import re
import time
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from robots import can_fetch
import sys
import json
from datetime import datetime
from connect_sql import connect_to_database  # Import the function here
import sqlite3

def insert_into_db(cursor, url, title, content, metadata):
    cursor.execute(
        'INSERT INTO "index" (url, title, content, last_crawled) VALUES (?, ?, ?, ?)',
        (url, title, content, datetime.now())
    )

def is_external_link(url, seed_url):
    return urlparse(url).netloc != urlparse(seed_url).netloc

def crawl(seed_url, search_term, synonyms, max_results=5, max_depth=3):
    conn, cursor = connect_to_database()
    crawled_urls = set()
    external_urls_to_crawl = deque([(seed_url, 0)])
    internal_urls_to_crawl = deque()
    results = []
    user_agent = 'YourCrawlerBot/1.0'

    session = requests.Session()
    retries = Retry(total=5, backoff_factor=1, status_forcelist=[429])
    session.mount('http://', HTTPAdapter(max_retries=retries))
    session.mount('https://', HTTPAdapter(max_retries=retries))

    while (external_urls_to_crawl or internal_urls_to_crawl) and len(results) < max_results:
        if external_urls_to_crawl:
            current_url, depth = external_urls_to_crawl.popleft()
        else:
            current_url, depth = internal_urls_to_crawl.popleft()

        if current_url in crawled_urls or depth > max_depth:
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
            results.append((current_url, title))
            insert_into_db(cursor, current_url, title, page_text, {})

        crawled_urls.add(current_url)
        for link in soup.find_all('a', href=True):
            href = link['href']
            absolute_url = urljoin(current_url, href)
            if absolute_url not in crawled_urls:
                if is_external_link(absolute_url, seed_url):
                    external_urls_to_crawl.append((absolute_url, depth + 1))
                else:
                    internal_urls_to_crawl.append((absolute_url, depth + 1))

        time.sleep(1)

    conn.commit()
    conn.close()
    return results
