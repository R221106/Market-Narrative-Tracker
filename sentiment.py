from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()

def get_sentiment(text):
    if not text or not text.strip():
        return {"label": "neutral", "score": 0.0}

    scores = analyzer.polarity_scores(text)
    compound = scores["compound"]

    if compound >= 0.05:
        label = "positive"
    elif compound <= -0.05:
        label = "negative"
    else:
        label = "neutral"

    return {
        "label": label,
        "score": round(compound, 3),
        "detail": scores
    }

def analyze_articles(articles):
    if not articles:
        return {"label": "neutral", "score": 0.0}

    total_score = 0
    for article in articles:
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

# NEW function — scores each article individually
def analyze_articles_individually(articles):
    if not articles:
        return []

    scored = []
    for article in articles:
        title = article.get("title", "") or ""
        description = article.get("description", "") or ""
        text = f"{title}. {description}"
        result = get_sentiment(text)

        scored.append({
            "title":       title,
            "description": article.get("description", ""),
            "url":         article.get("url", ""),
            "source":      article.get("source", ""),
            "publishedAt": article.get("publishedAt", ""),
            "sentiment":   result["label"],
            "score":       result["score"]
        })

    # sort by score — most positive first
    scored.sort(key=lambda x: x["score"], reverse=True)
    return scored