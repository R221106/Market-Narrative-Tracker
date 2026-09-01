import requests

from config import (
    CURRENTS_API_KEY,
    CURRENTS_BASE_URL,
    CURRENTS_MAX_RESULTS,
    NEWS_API_TIMEOUT
)


# ============================================================
# FETCH CURRENTS
# ============================================================

def fetch_currents(topic):

    if not topic or not topic.strip():
        return []

    params = {
        "keywords": topic,
        "language": "en",
        "page_size": CURRENTS_MAX_RESULTS,
        "apiKey": CURRENTS_API_KEY
    }

    try:

        response = requests.get(
            CURRENTS_BASE_URL,
            params=params,
            timeout=NEWS_API_TIMEOUT
        )

        response.raise_for_status()

        data = response.json()

    except requests.exceptions.Timeout:

        print(f"Currents timed out for: {topic}")
        return []

    except requests.exceptions.RequestException as e:

        print(f"Currents error for {topic}: {e}")
        return []

    articles = data.get("news", [])

    return [
        {
            "title": article.get("title") or "No title",
            "description": article.get("description") or "",
            "content": article.get("description") or "",
            "url": article.get("url") or "",
            "source": article.get("author") or "Unknown",
            "publishedAt": article.get("published") or "",
            "provider": "currents"
        }

        for article in articles
    ]


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    results = fetch_currents("AI")

    print(
        f"Currents returned "
        f"{len(results)} articles"
    )

    for article in results[:5]:

        print(
            f"[{article['source']}] "
            f"{article['title']}"
        )
