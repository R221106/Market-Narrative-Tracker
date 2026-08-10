from flask import Flask, jsonify
from flask_cors import CORS
from news_fetcher import fetch_news

app = Flask(__name__)
CORS(app)


@app.route("/")
def home():
    return "Market Narrative Tracker — backend running"


@app.route("/api/news")
def news():
    articles = fetch_news("Artificial Intelligence")

    return jsonify({
        "topic": "AI",
        "articles": articles
    })


if __name__ == "__main__":
    app.run(debug=True)