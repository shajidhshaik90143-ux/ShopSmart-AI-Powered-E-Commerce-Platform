POSITIVE = {
    "good", "great", "excellent", "amazing", "awesome", "love",
    "perfect", "best", "happy", "fast", "quality", "nice", "worth"
}
NEGATIVE = {
    "bad", "poor", "terrible", "worst", "hate", "slow",
    "broken", "expensive", "disappointed", "problem", "late"
}

def analyze_sentiment(text):
    words = {w.strip(".,!?;:").lower() for w in text.split()}
    pos = len(words & POSITIVE)
    neg = len(words & NEGATIVE)
    if pos > neg:
        return "positive"
    if neg > pos:
        return "negative"
    return "neutral"
