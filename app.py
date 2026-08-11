from flask import Flask, jsonify, request
from flask_cors import CORS
from news_fetcher import fetch_news

app = Flask(__name__)
CORS(app)


@app.route("/")
def home():
    return "Market Narrative Tracker — backend running"


@app.route("/api/news")
def news():
    topic = request.args.get("topic", "AI")

    articles = fetch_news(topic)

    return jsonify({
        "topic": topic,
        "articles": articles
    })


if __name__ == "__main__":
    app.run(debug=True)