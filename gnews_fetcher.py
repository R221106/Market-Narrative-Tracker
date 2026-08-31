import requests
from config import GNEWS_API_KEY, GNEWS_BASE_URL, GNEWS_MAX_RESULTS, NEWS_API_TIMEOUT

def fetch_gnews(topic):
    if not topic or not topic.strip():
        return []

    params = {
        "q":      topic,
        "lang":   "en",
        "sortby": "publishedAt",
        "max":    GNEWS_MAX_RESULTS,
        "apikey": GNEWS_API_KEY
    }

    try:
        response = requests.get(
            GNEWS_BASE_URL,
            params=params,
            timeout=NEWS_API_TIMEOUT
        )
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.Timeout:
        print(f"GNews timed out for: {topic}")
        return []
    except requests.exceptions.RequestException as e:
        print(f"GNews error for {topic}: {e}")
        return []

    return [
        {
            "title":       a.get("title") or "No title",
            "description": a.get("description") or "",
            "content":     a.get("content") or "",
            "url":         a.get("url") or "",
            "source":      (a.get("source") or {}).get("name") or "Unknown",
            "publishedAt": a.get("publishedAt") or "",
            "provider":    "gnews"
        }
        for a in data.get("articles", [])
    ]

if __name__ == "__main__":
    results = fetch_gnews("AI")
    print(f"GNews returned {len(results)} articles")
    for a in results[:5]:
        print(f"[{a['source']}] {a['title']}")
