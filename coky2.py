#!/usr/bin/env python3

import sys
from synonyms import get_synonyms
from web_crawler import crawl
from crawl_state import get_next_url_from_crawl_state

def check_stop_flag():
    try:
        with open('stop_flag.txt', 'r') as f:
            return f.read().strip() == '1'
    except Exception as e:
        print(f"Error reading stop flag: {e}")
        return False

def main():
    if len(sys.argv) < 3:
        print("Usage: python3 coky2.py <search_term> <max_depth>")
        sys.exit(1)

    search_term = sys.argv[1]
    max_depth = int(sys.argv[2])

    try:
        while True:
            seed_url = get_next_url_from_crawl_state()
            if not seed_url:
                print("No URLs found in crawl_state. Exiting.")
                break

            print(f"Crawling URL: {seed_url}, Depth: 0")
            results = crawl(seed_url, search_term, get_synonyms(search_term), max_depth=max_depth)

            if results:
                print("\nSearch Results:")
                for url, title in results:
                    print(f"URL: {url}\nTitle: {title}\n")

            # After crawling, check if we should continue
            if check_stop_flag():
                print("Crawling stopped by user.")
                break

    except Exception as ex:
        print(f"Exception in main: {ex}")
    finally:
        print("Main: Entering the finally block.")
        with open('status_flag.txt', 'w') as f:
            f.write('Crawling completed.')
        print("Main: Finally block completed.")

if __name__ == "__main__":
    main()
