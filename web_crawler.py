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

def get_synonyms(word):
    # Your synonym fetching logic here
    return [word]

def is_external_link(url, base_url):
    return urlparse(url).netloc != urlparse(base_url).netloc

def is_valid_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False

def crawl(seed_url, search_term, synonyms, max_results=10, max_depth=5):
    crawled_urls = set()
    external_urls_to_crawl = deque([(seed_url, 0)])
    internal_urls_to_crawl = deque()
    results = []
    user_agent = 'YourCrawlerBot/1.0'

    # Session with retry mechanism
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
        except requests.HTTPError as e:
            if response.status_code == 403:
                print(f"Access forbidden (403) for URL: {current_url}")
            else:
                print(f"HTTP error {response.status_code} while crawling {current_url}: {e}")
            continue
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
            href = link['href']
            # Skip links that are not valid URLs
            if not href or href.startswith('javascript:') or href.startswith('#'):
                continue

            # Skip invalid hrefs
            try:
                absolute_url = urljoin(current_url, href)
                parsed_url = urlparse(absolute_url)
                if not all([parsed_url.scheme, parsed_url.netloc]):
                    continue
            except Exception as e:
                print(f"Error parsing URL: {href} - {e}")
                continue

            if absolute_url not in crawled_urls:
                if is_external_link(absolute_url, seed_url):
                    external_urls_to_crawl.append((absolute_url, depth + 1))
                else:
                    internal_urls_to_crawl.append((absolute_url, depth + 1))

        # Introduce a delay to avoid rate limiting
        time.sleep(1)  # 1 second delay between requests

    return results

# Example usage
if __name__ == "__main__":
    seed_url = input("Enter a seed URL: ")
    search_term = input("Enter a search term: ")
    synonyms = get_synonyms(search_term)
    results = crawl(seed_url, search_term, synonyms)
    print("\nSearch Results:")
    for url, title in results:
        print(f"URL: {url}\nTitle: {title}\n")
