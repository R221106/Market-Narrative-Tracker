from flask import Flask, jsonify, request

from flask_cors import CORS

from news_fetcher import fetch_news

from sentiment import (
    analyze_articles,
    analyze_articles_individually
)

from keywords import extract_keywords

from trend import analyze_trend

from sources import analyze_sources

from database import (
    init_db,
    get_popular_topics
)

from config import (
    DEFAULT_TOPIC,
    WATCHLIST_TOPICS
)


# ============================================================
# FLASK APP
# ============================================================

app = Flask(__name__)

CORS(app)


<<<<<<< HEAD
# ============================================================
# DATABASE
# ============================================================
=======
    articles = fetch_news(topic)
    overall = analyze_articles(articles)
    individual = analyze_articles_individually(articles)

    return jsonify({
        "topic": topic,
        "overall": overall,
        "articles": individual
    })

@app.route("/")
def home():
    return "Market Narrative Tracker — backend running"

@app.route("/api/dashboard")
def dashboard():
    topics = ["AI", "Nvidia", "Bitcoin", "Oil", "Tesla"]
    counts = []

    for topic in topics:
        articles = fetch_news(topic)
        counts.append(len(articles))

    return jsonify({
        "topics": topics,
        "counts": counts
    })

@app.route("/api/news")
def news():
    topic = request.args.get("topic", "AI").strip()

    if not topic:
        return jsonify({
            "error": "Topic cannot be empty"
        }), 400

    articles = fetch_news(topic)

    return jsonify({
        "topic": topic,
        "articles": articles
    })

@app.route("/api/keywords")
def keywords():
    topic = request.args.get("topic", "AI").strip()
    if not topic:
        return jsonify({"error": "Topic cannot be empty"}), 400

    articles = fetch_news(topic)
    top_keywords = extract_keywords(articles, top_n=10)

    return jsonify({
        "topic": topic,
        "count": len(top_keywords),
        "keywords": top_keywords
    })

@app.route("/api/trend")
def trend():
    topic = request.args.get("topic", "Bitcoin").strip()
    if not topic:
        return jsonify({"error": "Topic cannot be empty"}), 400

    articles = fetch_news(topic)
    result = analyze_trend(articles, topic)

    return jsonify(result)

@app.route("/api/sources")
def sources():
    topic = request.args.get("topic", "AI").strip()
    if not topic:
        return jsonify({"error": "Topic cannot be empty"}), 400

    articles = fetch_news(topic)
    top_sources = analyze_sources(articles)

    return jsonify({
        "topic": topic,
        "sources": top_sources
    })
>>>>>>> 9278b7123b14f87802391933055a7c17b89735fd

init_db()


# ============================================================
# SHARED TOPIC VALIDATION
# ============================================================

def get_topic():
    """
    Read and validate the topic from the request.
    """

    topic = request.args.get(
        "topic",
        DEFAULT_TOPIC
    ).strip()

    return topic or None


def topic_error():

    return jsonify({
        "error": "Topic cannot be empty"
    }), 400


# ============================================================
# HOME
# ============================================================

@app.route("/")
def home():

    return "Market Narrative Tracker — backend running"


# ============================================================
# NEWS
# ============================================================

@app.route("/api/news")
def news():

    topic = get_topic()

    if not topic:

        return topic_error()

    articles = fetch_news(topic)

    return jsonify({

        "topic": topic,

        "articles": articles
    })


# ============================================================
# SENTIMENT
# ============================================================

@app.route("/api/sentiment")
def sentiment():

    topic = get_topic()

    if not topic:

        return topic_error()

    articles = fetch_news(topic)

    overall = analyze_articles(
        articles
    )

    individual = (
        analyze_articles_individually(
            articles
        )
    )

    return jsonify({

        "topic": topic,

        "overall": overall,

        "articles": individual
    })


# ============================================================
# KEYWORDS
# ============================================================

@app.route("/api/keywords")
def keywords():

    topic = get_topic()

    if not topic:

        return topic_error()

    articles = fetch_news(topic)

    top_keywords = extract_keywords(
        articles
    )

    return jsonify({

        "topic": topic,

        "count": len(top_keywords),

        "keywords": top_keywords
    })


# ============================================================
# TREND
# ============================================================

@app.route("/api/trend")
def trend():

    topic = get_topic()

    if not topic:

        return topic_error()

    articles = fetch_news(topic)

    return jsonify(
        analyze_trend(
            articles,
            topic
        )
    )


# ============================================================
# SOURCES
# ============================================================

@app.route("/api/sources")
def sources():

    topic = get_topic()

    if not topic:

        return topic_error()

    articles = fetch_news(topic)

    return jsonify({

        "topic": topic,

        "sources": analyze_sources(
            articles
        )
    })


# ============================================================
# WATCHLIST TOPICS
# ============================================================

@app.route("/api/topics")
def topics():

    topic_data = []

    for topic in WATCHLIST_TOPICS:

        articles = fetch_news(topic)

        topic_data.append({

            "topic": topic,

            "article_count": len(
                articles
            )
        })

    topic_data.sort(
        key=lambda x: x["article_count"],
        reverse=True
    )

    return jsonify({

        "topics": topic_data
    })


# ============================================================
# POPULAR TOPICS
# ============================================================

@app.route("/api/popular")
def popular():

    return jsonify({

        "popular_topics":
            get_popular_topics(
                limit=5
            )
    })


# ============================================================
# DASHBOARD
# ============================================================

@app.route("/api/dashboard")
def dashboard():

    topic_data = []

    for topic in WATCHLIST_TOPICS:

        articles = fetch_news(topic)

        topic_data.append({

            "topic": topic,

            "article_count": len(
                articles
            )
        })

    topic_data.sort(
        key=lambda x: x["article_count"],
        reverse=True
    )

    counts = [

        item["article_count"]

        for item in topic_data
    ]

    labels = [

        item["topic"]

        for item in topic_data
    ]

    return jsonify({

        "topics": labels,

        "counts": counts
    })


# ============================================================
# RUN SERVER
# ============================================================

if __name__ == "__main__":

    app.run(debug=True)