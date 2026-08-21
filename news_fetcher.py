import requests

from database import save_articles, get_cached_articles, log_search

from config import (
    NEWS_API_KEY,
    NEWS_API_BASE_URL,
    NEWS_API_PAGE_SIZE,
    NEWS_API_TIMEOUT
)


def fetch_news(topic):
    """
    Fetch news articles for a topic.

    Uses SQLite cache first.
    If no valid cache exists, fetches fresh data from NewsAPI.
    """

    # --------------------------------------------------------
    # Validate topic
    # --------------------------------------------------------

    if not topic or not topic.strip():
        return []

    topic = topic.strip()

    # --------------------------------------------------------
    # Check cache
    # --------------------------------------------------------

    cached = get_cached_articles(topic)

    if cached:
        print(f"Cache hit for '{topic}'")
        return cached

    print(f"Cache miss for '{topic}' — fetching from NewsAPI")

    # --------------------------------------------------------
    # NewsAPI parameters
    # --------------------------------------------------------

    params = {
        "q": topic,
        "language": "en",
        "sortBy": "publishedAt",
        "pageSize": NEWS_API_PAGE_SIZE,
        "apiKey": NEWS_API_KEY
    }

    # --------------------------------------------------------
    # Make API request
    # --------------------------------------------------------

    try:

        response = requests.get(
            NEWS_API_BASE_URL,
            params=params,
            timeout=NEWS_API_TIMEOUT
        )

        response.raise_for_status()

        data = response.json()

    except requests.exceptions.Timeout:

        print(f"NewsAPI timed out for topic: {topic}")

        return []

    except requests.exceptions.RequestException as e:

        print(f"NewsAPI error for topic {topic}: {e}")

        return []

    # --------------------------------------------------------
    # Extract articles
    # --------------------------------------------------------

    articles = data.get("articles", [])

    # --------------------------------------------------------
    # Clean article data
    # --------------------------------------------------------

    clean_articles = [
        {
            "title": article.get("title") or "No title",
            "description": article.get("description") or "",
            "url": article.get("url") or "",
            "source": article.get("source", {}).get("name") or "Unknown",
            "publishedAt": article.get("publishedAt") or ""
        }

        for article in articles
    ]

    # --------------------------------------------------------
    # Save results
    # --------------------------------------------------------

    if clean_articles:

        save_articles(topic, clean_articles)

        log_search(
            topic,
            len(clean_articles)
        )

    return clean_articles