from spellchecker import SpellChecker

spell = SpellChecker()

def correct_spelling(search_term):
    corrected_words = []
    words = search_term.split()
    for word in words:
        corrected_word = spell.correction(word)
        corrected_words.append(corrected_word)
    return ' '.join(corrected_words)
