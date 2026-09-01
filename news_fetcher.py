from gnews_fetcher import fetch_gnews
from currents_fetcher import fetch_currents


# ============================================================
# MAIN NEWS FETCHER
# ============================================================

def fetch_news(topic):
    """
    Fetch news using a fallback system.

    Priority:
    1. GNews
    2. Currents API
    """

    if not topic or not topic.strip():
        return []

    # Use the value from config.py unless a value is supplied
    if max_articles is None:
        max_articles = GNEWS_MAX_RESULTS

    query = build_search_query(narrative)

    params = {
        "q": query,
        "lang": "en",
        "sortby": "publishedAt",
        "max": max_articles,
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

    print(
        f"⚠ GNews failed or returned no articles "
        f"for {topic}."
    )

    print("Trying Currents...")

    articles = fetch_currents(topic)

    if articles:
        print(
            f"✓ Currents returned "
            f"{len(articles)} articles"
        )

        return articles

    # ========================================================
    # NO RESULTS
    # ========================================================

    print(
        f"✗ All news providers failed "
        f"for: {topic}"
    )

    return []


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    results = fetch_news("AI")

    print(
        f"\nFinal result: "
        f"{len(results)} articles"
    )

    for article in results[:5]:
        print(
            f"[{article['provider']}] "
            f"{article['title']}"
        )
