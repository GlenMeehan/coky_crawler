import nltk
from nltk.corpus import wordnet

nltk.download('wordnet')

def get_synonyms(search_term):
    synonyms = []
    for syn in wordnet.synsets(search_term):
        for lemma in syn.lemmas():
            synonyms.append(lemma.name())
    return set(synonyms)
