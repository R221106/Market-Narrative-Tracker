import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("NEWS_API_KEY")
BASE_URL = "https://newsapi.org/v2/everything"


def fetch_news(topic):
    if not topic or not topic.strip():
        return []

    params = {
        "q": topic,
        "language": "en",
        "sortBy": "publishedAt",
        "pageSize": 10,
        "apiKey": API_KEY
    }

    try:
        response = requests.get(
            BASE_URL,
            params=params,
            timeout=5
        )

        response.raise_for_status()
        data = response.json()

    except requests.exceptions.Timeout:
        print("NewsAPI request timed out")
        return []

    except requests.exceptions.RequestException as e:
        print("NewsAPI request failed:", e)
        return []

    articles = data.get("articles", [])
    clean_articles=[
        {
        "title": article.get("title", "No title"),
        "description": article.get("description", ""),
        "url": article.get("url", ""),
        "source": article.get("source", {}).get("name", "Unknown"),
        "publishedAt": article.get("publishedAt", "")
        }
        for article in articles
    ]

    return clean_articles


if __name__ == "__main__":
    articles = fetch_news("Artificial Intelligence")

    for article in articles[:5]:
        print(article["title"])