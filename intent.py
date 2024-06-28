from textblob import TextBlob

def understand_intent(search_term):
    blob = TextBlob(search_term)
    sentiment = blob.sentiment
    return sentiment
