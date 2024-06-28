#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time
import re

def extract_title(soup):
    title_tag = soup.find('title')
    if title_tag:
        return title_tag.get_text()
    return "No title found"

def is_relevant(content, search_term):
    search_term = search_term.lower()
    # Check if search term is in the title
    title_tag = content.find('title')
    if title_tag and search_term in title_tag.get_text().lower():
        return True
    # Check if search term is in any heading tags
    for heading in content.find_all(re.compile('^h[1-6]$')):
        if search_term in heading.get_text().lower():
            return True
    # Check if search term is in the first 2000 characters of the body text
    if search_term in content.get_text()[:2000].lower():
        return True
    return False

def crawl(seed_url, search_term, max_relevant_pages=10):
    visited = set()
    to_visit = [seed_url]
    relevant_urls = []

    parsed_seed_url = urlparse(seed_url)
    base_domain = f"{parsed_seed_url.scheme}://{parsed_seed_url.netloc}"

    while to_visit and len(relevant_urls) < max_relevant_pages:
        current_url = to_visit.pop(0)
        if current_url in visited:
            continue

        print(f"Crawling: {current_url}")
        visited.add(current_url)

        try:
            response = requests.get(current_url)
            content_type = response.headers.get('Content-Type', '').lower()
            if 'text/html' not in content_type:
                continue

            soup = BeautifulSoup(response.content, 'html.parser')

            if is_relevant(soup, search_term):
                title = extract_title(soup)
                relevant_urls.append((current_url, title))
                print(f"Relevant page found: {current_url}")
                print(f"Title: {title}")

            # Add all links to the to_visit list regardless of relevance to keep crawling
            for link in soup.find_all('a', href=True):
                absolute_url = urljoin(current_url, link['href'])
                parsed_url = urlparse(absolute_url)
                if (parsed_url.scheme in {'http', 'https'}
                    and absolute_url not in visited
                    and absolute_url.startswith(base_domain)):
                    to_visit.append(absolute_url)

        except Exception as e:
            print(f"Exception while crawling {current_url}: {e}")

        time.sleep(1)  # Be polite and don't hammer the server with requests

    return relevant_urls

if __name__ == "__main__":
    seed_url = input("Enter a seed URL: ")
    search_term = input("Enter a search term: ")

    results = crawl(seed_url, search_term)

    print("\nSearch Results:")
    for url, title in results:
        print(f"URL: {url}")
        print(f"Title: {title}\n")
