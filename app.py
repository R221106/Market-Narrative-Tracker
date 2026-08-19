from flask import Flask, jsonify, request
from flask_cors import CORS
from news_fetcher import fetch_news
from sentiment import analyze_articles, analyze_articles_individually 
from keywords import extract_keywords
from trend import analyze_trend
from sources import analyze_sources
from database import init_db, get_popular_topics

app = Flask(__name__)
CORS(app)

@app.route("/api/sentiment")
def sentiment():
    topic = request.args.get("topic", "AI").strip()
    if not topic:
        return jsonify({"error": "Topic cannot be empty"}), 400

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

init_db()

@app.route("/api/popular")
def popular():
    topics = get_popular_topics(limit=5)
    return jsonify({"popular_topics": topics})

if __name__ == "__main__":
    app.run(debug=True)