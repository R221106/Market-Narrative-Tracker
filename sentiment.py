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
# FINANCIAL LEXICON
# ============================================================

FINANCIAL_LEXICON = {

    # --------------------------------------------------------
    # POSITIVE FINANCIAL TERMS
    # --------------------------------------------------------

    "bullish": 0.8,

    "bull": 0.6,

    "surge": 0.7,

    "surges": 0.7,

    "soar": 0.75,

    "soars": 0.75,

    "rally": 0.65,

    "rallies": 0.65,

    "boom": 0.7,

    "booming": 0.7,

    "breakthrough": 0.7,

    "outperform": 0.6,

    "upgrade": 0.5,

    "beat": 0.5,

    "beats": 0.5,

    "record": 0.4,

    "profit": 0.5,

    "profits": 0.5,

    "profitable": 0.6,

    "growth": 0.5,

    "gains": 0.5,

    "gain": 0.5,

    "strong": 0.4,

    "optimistic": 0.6,

    "positive": 0.5,


    # --------------------------------------------------------
    # NEGATIVE FINANCIAL TERMS
    # --------------------------------------------------------

    "bearish": -0.8,

    "bear": -0.6,

    "crash": -0.8,

    "crashes": -0.8,

    "collapse": -0.8,

    "collapses": -0.8,

    "plunge": -0.7,

    "plunges": -0.7,

    "slump": -0.6,

    "slumps": -0.6,

    "recession": -0.7,

    "downgrade": -0.6,

    "loss": -0.5,

    "losses": -0.55,

    "debt": -0.4,

    "bankrupt": -0.9,

    "bankruptcy": -0.9,

    "fraud": -0.85,

    "investigation": -0.5,

    "lawsuit": -0.5,

    "fine": -0.4,

    "tariff": -0.4,

    "tariffs": -0.4,

    "inflation": -0.5,

    "layoffs": -0.65,

    "layoff": -0.65,

    "decline": -0.5,

    "declines": -0.5,

    "weak": -0.4,

    "weakness": -0.5,

    "pessimistic": -0.6,


    # --------------------------------------------------------
    # FINANCIAL TERMS THAT SHOULD BE NEUTRAL
    # --------------------------------------------------------

    "market": 0.0,

    "trading": 0.0,

    "investors": 0.0,

    "shares": 0.0,

    "stock": 0.0,

    "stocks": 0.0,

    "equity": 0.0,

    "fund": 0.0,

    "funds": 0.0,

    "investment": 0.0,

    "investments": 0.0
}


# ============================================================
# APPLY FINANCIAL LEXICON
# ============================================================

def _apply_financial_lexicon():
    """
    Add financial terminology to VADER's dictionary.
    """

    analyzer.lexicon.update(
        FINANCIAL_LEXICON
    )


_apply_financial_lexicon()


# ============================================================
# SENTIMENT LABEL
# ============================================================

def _get_label(compound):

    if compound >= SENTIMENT_POSITIVE_THRESHOLD:

        return "positive"

    elif compound <= SENTIMENT_NEGATIVE_THRESHOLD:

        return "negative"

    return "neutral"


# ============================================================
# SINGLE TEXT SENTIMENT
# ============================================================

def get_sentiment(text):

    if not text or not text.strip():

        return {
            "label": "neutral",
            "score": 0.0
        }

    scores = analyzer.polarity_scores(
        text
    )

    compound = round(
        scores["compound"],
        3
    )

    return {

        "label": _get_label(
            compound
        ),

        "score": compound,

        "detail": scores
    }


# ============================================================
# OVERALL ARTICLE SENTIMENT
# ============================================================

def analyze_articles(articles):

    if not articles:

        return {
            "label": "neutral",
            "score": 0.0
        }

    scores = [

        get_sentiment(

            f"{article.get('title', '')}. "
            f"{article.get('description', '')}"

        )["score"]

        for article in articles
    ]

    average = round(
        sum(scores) / len(scores),
        3
    )

    return {

        "label": _get_label(
            average
        ),

        "score": average
    }


# ============================================================
# INDIVIDUAL ARTICLE SENTIMENT
# ============================================================

def analyze_articles_individually(articles):

    if not articles:

        return []

    scored = []

    for article in articles:

        text = (

            f"{article.get('title', '')}. "
            f"{article.get('description', '')}"

        ).strip()

        result = get_sentiment(
            text
        )

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

            "sentiment": result[
                "label"
            ],

            "score": result[
                "score"
            ]
        })

    return sorted(

        scored,

        key=lambda x: x["score"],

        reverse=True
    )


# ============================================================
# DAY 14 TESTING
# ============================================================

if __name__ == "__main__":

    test_cases = [

        (
            "Bitcoin crashes as regulators crack down on fraud",
            "negative"
        ),

        (
            "Nvidia surges to record high on AI boom",
            "positive"
        ),

        (
            "Fed raises rates amid inflation fears causing market slump",
            "negative"
        ),

        (
            "Tesla rally continues as EV sales beat expectations",
            "positive"
        ),

        (
            "Company files for bankruptcy after massive losses",
            "negative"
        ),

        (
            "Quantum computing breakthrough drives bullish sentiment",
            "positive"
        )
    ]


    print(
        "=== Financial Sentiment Tests ===\n"
    )


    for text, expected in test_cases:

        result = get_sentiment(
            text
        )

        actual = result[
            "label"
        ]

        if actual == expected:

            symbol = "✓"

        else:

            symbol = "✗"

        print(

            f"{symbol} "
            f"{actual:<10} "
            f"{result['score']:>7}  "
            f"{text}"
        )