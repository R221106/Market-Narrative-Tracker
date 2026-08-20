from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

from config import (
    SENTIMENT_POSITIVE_THRESHOLD,
    SENTIMENT_NEGATIVE_THRESHOLD
)


# ============================================================
# VADER ANALYZER
# ============================================================

analyzer = SentimentIntensityAnalyzer()


# ============================================================
# SENTIMENT LABEL
# ============================================================

def _get_label(compound):
    """
    Convert a VADER compound score into a sentiment label.
    """

    if compound >= SENTIMENT_POSITIVE_THRESHOLD:

        return "positive"

    elif compound <= SENTIMENT_NEGATIVE_THRESHOLD:

        return "negative"

    return "neutral"


# ============================================================
# SINGLE TEXT SENTIMENT
# ============================================================

def get_sentiment(text):
    """
    Analyse sentiment of one piece of text.
    """

    if not text or not text.strip():

        return {
            "label": "neutral",
            "score": 0.0
        }

    scores = analyzer.polarity_scores(text)

    compound = round(
        scores["compound"],
        3
    )

    return {
        "label": _get_label(compound),
        "score": compound,
        "detail": scores
    }


# ============================================================
# OVERALL ARTICLE SENTIMENT
# ============================================================

def analyze_articles(articles):
    """
    Calculate average sentiment across all articles.
    """

    if not articles:

        return {
            "label": "neutral",
            "score": 0.0
        }

    scores = []

    for article in articles:

        text = (
            f"{article.get('title', '')}. "
            f"{article.get('description', '')}"
        ).strip()

        result = get_sentiment(text)

        scores.append(result["score"])

    average = round(
        sum(scores) / len(scores),
        3
    )

    return {
        "label": _get_label(average),
        "score": average
    }


# ============================================================
# INDIVIDUAL ARTICLE SENTIMENT
# ============================================================

def analyze_articles_individually(articles):
    """
    Calculate sentiment for each individual article.
    """

    if not articles:

        return []

    scored = []

    for article in articles:

        text = (
            f"{article.get('title', '')}. "
            f"{article.get('description', '')}"
        ).strip()

        result = get_sentiment(text)

        scored.append({

            "title": article.get(
                "title",
                ""
            ),

            "description": article.get(
                "description",
                ""
            ),

            "url": article.get(
                "url",
                ""
            ),

            "source": article.get(
                "source",
                ""
            ),

            "publishedAt": article.get(
                "publishedAt",
                ""
            ),

            "sentiment": result["label"],

            "score": result["score"]
        })

    return sorted(
        scored,
        key=lambda x: x["score"],
        reverse=True
    )