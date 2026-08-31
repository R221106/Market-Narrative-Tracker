import os
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from news_fetcher import fetch_news
from sentiment import analyze_articles, analyze_articles_individually
from keywords import extract_keywords
from trend import analyze_trend
from sources import analyze_sources
from database import init_db, get_popular_topics
from config import DEFAULT_TOPIC, WATCHLIST_TOPICS
from summariser import generate_summary

# ============================================================
# FLASK APP
# ============================================================

app = Flask(__name__, static_folder="static", static_url_path="")
CORS(app)
init_db()

# ============================================================
# SHARED TOPIC VALIDATION
# ============================================================

def get_topic():
    topic = request.args.get("topic", DEFAULT_TOPIC).strip()
    return topic or None

def topic_error():
    return jsonify({"error": "Topic cannot be empty"}), 400

# ============================================================
# FRONTEND PAGES
# ============================================================

@app.route("/")
def home():
    return send_from_directory("static", "index.html")

@app.route("/dashboard.html")
def dashboard_page():
    return send_from_directory("static", "dashboard.html")

@app.route("/search.html")
def search_page():
    return send_from_directory("static", "search.html")

@app.route("/Images/<path:filename>")
def images(filename):
    return send_from_directory("Images", filename)

@app.route("/Videos/<path:filename>")
def videos(filename):
    return send_from_directory("Videos", filename)

# ============================================================
# HEALTH
# ============================================================

@app.route("/api/health")
def health():
    return jsonify({"status": "healthy", "service": "Market Narrative Tracker"}), 200

# ============================================================
# NEWS
# ============================================================

@app.route("/api/news")
def news():
    topic = get_topic()
    if not topic:
        return topic_error()
    return jsonify({"topic": topic, "articles": fetch_news(topic)})

# ============================================================
# SENTIMENT
# ============================================================

@app.route("/api/sentiment")
def sentiment():
    topic = get_topic()
    if not topic:
        return topic_error()
    articles = fetch_news(topic)
    return jsonify({
        "topic":    topic,
        "overall":  analyze_articles(articles),
        "articles": analyze_articles_individually(articles)
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
    top_keywords = extract_keywords(articles)
    return jsonify({"topic": topic, "count": len(top_keywords), "keywords": top_keywords})

# ============================================================
# TREND
# ============================================================

@app.route("/api/trend")
def trend():
    topic = get_topic()
    if not topic:
        return topic_error()
    return jsonify(analyze_trend(fetch_news(topic), topic))

# ============================================================
# SOURCES
# ============================================================

@app.route("/api/sources")
def sources():
    topic = get_topic()
    if not topic:
        return topic_error()
    return jsonify({"topic": topic, "sources": analyze_sources(fetch_news(topic))})

# ============================================================
# WATCHLIST TOPICS
# ============================================================

@app.route("/api/topics")
def topics():
    topic_data = []
    for t in WATCHLIST_TOPICS:
        articles = fetch_news(t)
        topic_data.append({"topic": t, "article_count": len(articles)})
    topic_data.sort(key=lambda x: x["article_count"], reverse=True)
    return jsonify({"topics": topic_data})

# ============================================================
# POPULAR TOPICS
# ============================================================

@app.route("/api/popular")
def popular():
    return jsonify({"popular_topics": get_popular_topics(limit=5)})

# ============================================================
# DASHBOARD DATA
# ============================================================

@app.route("/api/dashboard")
def dashboard():
    topic_data = []
    for t in WATCHLIST_TOPICS:
        articles = fetch_news(t)
        topic_data.append({"topic": t, "article_count": len(articles)})
    topic_data.sort(key=lambda x: x["article_count"], reverse=True)
    return jsonify({
        "topics": [i["topic"] for i in topic_data],
        "counts": [i["article_count"] for i in topic_data]
    })

# ============================================================
# SUMMARY
# ============================================================

@app.route("/api/summary")
def summary():
    topic = get_topic()
    if not topic:
        return topic_error()
    articles = fetch_news(topic)
    sentiment = analyze_articles(articles)
    kws = extract_keywords(articles, top_n=5)
    narrative = generate_summary(
        topic=topic,
        articles=articles,
        sentiment_label=sentiment["label"],
        top_keywords=kws
    )
    return jsonify({
        "topic":     topic,
        "summary":   narrative,
        "sentiment": sentiment["label"],
        "keywords":  [kw["word"] for kw in kws]
    })

# ============================================================
# RUN SERVER
# ============================================================

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    debug = not os.environ.get("RENDER", False)
    app.run(host="0.0.0.0", port=port, debug=debug)