#!/usr/bin/env python3

import nltk
from spell_correction import correct_spelling
from synonyms import get_synonyms
from web_crawler import crawl
from connect_sql import connect_to_database
from crawl_state import get_next_url_from_crawl_state, save_crawl_state

# Ensure necessary NLTK data is downloaded
nltk.download('wordnet')

def main():
    search_term = input("Enter a search term: ")
    corrected_search_term = correct_spelling(search_term)
    print(f"Corrected Search Term: {corrected_search_term}")

    synonyms = get_synonyms(corrected_search_term)
    print(f"Synonyms: {synonyms}")

    while True:
        next_url = get_next_url_from_crawl_state()
        if not next_url:
            print("No URLs found in crawl_state. Exiting.")
            break

        print(f"Crawling URL: {next_url}, Depth: 0")
        results = crawl(next_url, corrected_search_term, synonyms)

        print("\nSearch Results:")
        for url, title in results:
            print(f"URL: {url}\nTitle: {title}\n")

if __name__ == "__main__":
    main()
