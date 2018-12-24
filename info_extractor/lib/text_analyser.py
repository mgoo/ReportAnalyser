from textblob import TextBlob


def semantic_analysis(text):
    blob = TextBlob(text)
    return blob.sentiment.polarity