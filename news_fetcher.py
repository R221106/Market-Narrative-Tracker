import requests
import os
from dotenv import load_dotenv
from database import save_articles, get_cached_articles, log_search

load_dotenv()

API_KEY = os.getenv("NEWS_API_KEY")
BASE_URL = "https://newsapi.org/v2/everything"

def fetch_news(topic):
    if not topic or not topic.strip():
        return []

    # check cache first
    cached = get_cached_articles(topic)
    if cached:
        print(f"Cache hit for '{topic}' — serving {len(cached)} articles from DB")
        return cached

    # cache miss — call NewsAPI
    print(f"Cache miss for '{topic}' — fetching from NewsAPI")
    params = {
        "q": topic,
        "language": "en",
        "sortBy": "publishedAt",
        "pageSize": 10,
        "apiKey": API_KEY
    }

    try:
        response = requests.get(BASE_URL, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.Timeout:
        return []
    except requests.exceptions.RequestException:
        return []

    articles = data.get("articles", [])
    clean_articles = []
    for article in articles:
        clean_articles.append({
            "title":       article.get("title", "No title"),
            "description": article.get("description", ""),
            "url":         article.get("url", ""),
            "source":      article.get("source", {}).get("name", "Unknown"),
            "publishedAt": article.get("publishedAt", "")
        })

    # save to database before returning
    if clean_articles:
        save_articles(topic, clean_articles)
        log_search(topic, len(clean_articles))

    return clean_articles

if __name__ == "__main__":
    fetch_news("Artificial Intelligence")