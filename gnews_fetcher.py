import requests
from config import GNEWS_API_KEY, GNEWS_BASE_URL, GNEWS_MAX_RESULTS, NEWS_API_TIMEOUT

def fetch_gnews(topic):
    """fetch articles from GNews API for a given topic"""
    if not topic or not topic.strip():
        return []

    params = {
        "q":        topic,
        "lang":     "en",
        "sortby":   "publishedAt",
        "max":      GNEWS_MAX_RESULTS,
        "apikey":   GNEWS_API_KEY
    }

    try:
        response = requests.get(GNEWS_BASE_URL, params=params, timeout=NEWS_API_TIMEOUT)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.Timeout:
        print(f"GNews timed out for topic: {topic}")
        return []
    except requests.exceptions.RequestException as e:
        print(f"GNews error for topic {topic}: {e}")
        return []

    articles = data.get("articles", [])

    # normalise to same shape as NewsAPI articles
    clean_articles = [
        {
            "title":       article.get("title") or "No title",
            "description": article.get("description") or "",
            "url":         article.get("url") or "",
            "source":      article.get("source", {}).get("name") or "Unknown",
            "publishedAt": article.get("publishedAt") or "",
            "provider":    "gnews"   # tag so you know which source it came from
        }
        for article in articles
    ]

    return clean_articles


if __name__ == "__main__":
    results = fetch_gnews("Artificial Intelligence")
    print(f"GNews returned {len(results)} articles\n")
    for article in results[:5]:
        print(f"[{article['source']}] {article['title']}")