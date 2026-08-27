import requests
from database import save_articles, get_cached_articles, log_search
from gnews_fetcher import fetch_gnews
from config import (
    NEWS_API_KEY, NEWS_API_BASE_URL,
    NEWS_API_PAGE_SIZE, NEWS_API_TIMEOUT
)

def fetch_from_newsapi(topic):
    """fetch from NewsAPI — original source"""
    params = {
        "q":        topic,
        "language": "en",
        "sortBy":   "publishedAt",
        "pageSize": NEWS_API_PAGE_SIZE,
        "apiKey":   NEWS_API_KEY
    }
    try:
        response = requests.get(NEWS_API_BASE_URL, params=params, timeout=NEWS_API_TIMEOUT)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.Timeout:
        print(f"NewsAPI timed out for topic: {topic}")
        return []
    except requests.exceptions.RequestException as e:
        print(f"NewsAPI error: {e}")
        return []

    return [
        {
            "title":       a.get("title") or "No title",
            "description": a.get("description") or "",
            "url":         a.get("url") or "",
            "source":      a.get("source", {}).get("name") or "Unknown",
            "publishedAt": a.get("publishedAt") or "",
            "provider":    "newsapi"
        }
        for a in data.get("articles", [])
    ]

def deduplicate(articles):
    """remove articles with duplicate titles"""
    seen_titles = set()
    unique = []
    for article in articles:
        title = article.get("title", "").strip().lower()
        if title and title not in seen_titles:
            seen_titles.add(title)
            unique.append(article)
    return unique

def fetch_news(topic):
    if not topic or not topic.strip():
        return []

    # check cache first
    cached = get_cached_articles(topic)
    if cached:
        print(f"Cache hit for '{topic}' — {len(cached)} articles from DB")
        return cached

    print(f"Cache miss for '{topic}' — fetching from both sources")

    # fetch from both APIs simultaneously
    newsapi_articles = fetch_from_newsapi(topic)
    gnews_articles   = fetch_gnews(topic)

    # merge and deduplicate
    all_articles = deduplicate(newsapi_articles + gnews_articles)

    # sort merged results by date — newest first
    all_articles.sort(
        key=lambda x: x.get("publishedAt", ""),
        reverse=True
    )

    print(f"NewsAPI: {len(newsapi_articles)} | GNews: {len(gnews_articles)} | Merged: {len(all_articles)}")

    if all_articles:
        save_articles(topic, all_articles)
        log_search(topic, len(all_articles))

    return all_articles