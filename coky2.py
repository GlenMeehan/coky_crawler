#!/usr/bin/env python3

import nltk
from spell_correction import correct_spelling
from synonyms import get_synonyms
# from intent import understand_intent (optional, if you want to use it)
from web_crawler import crawl

# Ensure necessary NLTK data is downloaded
nltk.download('wordnet')

def main():
    seed_url = input("Enter a seed URL: ")
    search_term = input("Enter a search term: ")

    corrected_search_term = correct_spelling(search_term)
    print(f"Corrected Search Term: {corrected_search_term}")

    synonyms = get_synonyms(corrected_search_term)
    print(f"Synonyms: {synonyms}")

    results = crawl(seed_url, corrected_search_term, synonyms)

    print("\nSearch Results:")
    for url, title in results:
        print(f"URL: {url}\nTitle: {title}\n")

if __name__ == "__main__":
    main()
