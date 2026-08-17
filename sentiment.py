from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()

def get_sentiment(text):
    if not text or not text.strip():
        return {"label": "neutral", "score": 0.0}

    scores = analyzer.polarity_scores(text)
    compound = scores["compound"]

    # compound score rules:
    # >= 0.05  → positive
    # <= -0.05 → negative
    # in between → neutral
    if compound >= 0.05:
        label = "positive"
    elif compound <= -0.05:
        label = "negative"
    else:
        label = "neutral"

    return {
        "label": label,
        "score": round(compound, 3),
        "detail": scores  # shows pos, neg, neu, compound breakdown
    }

def analyze_articles(articles):
    if not articles:
        return {"label": "neutral", "score": 0.0}

    total_score = 0
    for article in articles:
        # combine title + description for better accuracy
        title = article.get("title", "") or ""
        description = article.get("description", "") or ""
        text = f"{title}. {description}"
        result = get_sentiment(text)
        total_score += result["score"]

    average_score = round(total_score / len(articles), 3)

    if average_score >= 0.05:
        label = "positive"
    elif average_score <= -0.05:
        label = "negative"
    else:
        label = "neutral"

    return {
        "label": label,
        "score": average_score
    }

# test it directly when you run this file
if __name__ == "__main__":
    test_strings = [
        "AI is revolutionizing the market and driving massive growth",
        "Markets crash as inflation fears grow and investors panic",
        "The company released a quarterly earnings report today",
        "Bitcoin surges to all time high amid investor optimism",
        "Regulators crack down on crypto exchanges over fraud concerns"
    ]

    print("=== VADER Sentiment Tests ===\n")
    for text in test_strings:
        result = get_sentiment(text)
        print(f"Text: {text[:50]}...")
        print(f"Label: {result['label']} | Score: {result['score']}")
        print(f"Detail: {result['detail']}\n")