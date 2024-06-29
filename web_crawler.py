import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from collections import deque
import re
from robots import can_fetch

def crawl(seed_url, search_term, synonyms, max_results=10, max_depth=3):
    crawled_urls = set()
    urls_to_crawl = deque([(seed_url, 0)])
    results = []
    user_agent = 'CokyCrawler/1.0 (+https://github.com/GlenMeehan/coky_crawler; contact@example.com)'

    while urls_to_crawl and len(results) < max_results:
        current_url, depth = urls_to_crawl.popleft()
        if current_url in crawled_urls or depth > max_depth:
            continue

        if not can_fetch(current_url, user_agent):
            print(f"Disallowed by robots.txt: {current_url}")
            continue

        try:
            response = requests.get(current_url, headers={'User-Agent': user_agent})
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"Exception while crawling {current_url}: {e}")
            continue

        soup = BeautifulSoup(response.content, 'html.parser')
        title = soup.title.string if soup.title else "No Title"
        page_text = soup.get_text()

        if re.search(search_term, page_text, re.IGNORECASE) or any(re.search(synonym, page_text, re.IGNORECASE) for synonym in synonyms):
            results.append((current_url, title))

        crawled_urls.add(current_url)
        for link in soup.find_all('a', href=True):
            absolute_url = urljoin(current_url, link['href'])
            # Allow the crawler to follow external links as well
            urls_to_crawl.append((absolute_url, depth + 1))

    return results
