import requests

from config import (
    GNEWS_API_KEY,
    GNEWS_BASE_URL,
    GNEWS_MAX_RESULTS,
    NEWS_API_TIMEOUT
)


# ============================================================
# SEARCH QUERY
# ============================================================

def build_search_query(narrative):
    """
    Builds a GNews query designed to find
    market-related news for the selected narrative.
    """

    queries = {

        "AI": (
            '"artificial intelligence" OR '
            '"generative AI" OR '
            '"machine learning" OR '
            '"large language model" OR '
            'LLM OR '
            'Nvidia OR '
            '"AI infrastructure"'
        ),

        "EV": (
            '("electric vehicle" OR "electric vehicles" OR '
            'EV OR EVs OR battery OR Tesla OR BYD OR '
            '"charging infrastructure") '
            'AND (market OR investment OR investor OR '
            'company OR industry OR sales OR earnings OR '
            'revenue OR demand OR regulation OR tariff)'
        ),

        "Quantum Computing": (
            '("quantum computing" OR "quantum computer" OR '
            '"quantum technology" OR "quantum processor") '
            'AND (market OR investment OR investor OR '
            'company OR industry OR funding OR revenue OR '
            'technology OR regulation)'
        ),

        "Semiconductors": (
            '(semiconductor OR semiconductors OR chip OR '
            'chips OR Nvidia OR AMD OR Intel OR TSMC OR '
            'GPU OR processor OR foundry) '
            'AND (market OR investment OR investor OR '
            'company OR industry OR earnings OR revenue OR '
            'demand OR supply OR manufacturing OR tariff)'
        )
    }

    return queries.get(
        narrative,
        f'"{narrative}" AND '
        '(market OR investment OR investor OR '
        'company OR industry OR earnings OR revenue)'
    )


# ============================================================
# FETCH GNEWS
# ============================================================

def fetch_news(narrative, max_articles=None):
    """
    Fetch candidate articles from GNews.

    This function retrieves potential articles.
    Relevance filtering is handled separately by news_filter.py.
    """

    if not narrative or not narrative.strip():
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

    ## If GNews Hit the Limit !
    except requests.exceptions.HTTPError as e:
        print(
            f"GNews HTTP error for topic {narrative}: {e}"
        )
        if response.status_code in (403, 429):
            return None
        return []

    except requests.exceptions.Timeout:

        print(
            f"GNews timed out for topic: {narrative}"
        )

        return []

    except requests.exceptions.RequestException as e:

        print(
            f"GNews error for topic {narrative}: {e}"
        )

        return []

    articles = data.get("articles", [])

    # ========================================================
    # NORMALISE GNEWS RESPONSE
    # ========================================================

    clean_articles = []

    for article in articles:

        source = article.get("source") or {}

        clean_articles.append({
            "title": article.get("title") or "No title",

            "description": (
                article.get("description") or ""
            ),

            "content": (
                article.get("content") or ""
            ),

            "url": article.get("url") or "",

            "source": (
                source.get("name")
                or "Unknown"
            ),

            "publishedAt": (
                article.get("publishedAt")
                or ""
            ),

            "provider": "gnews"
        })

    return clean_articles


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    results = fetch_news("AI")

    print(
        f"GNews returned {len(results)} candidate articles\n"
    )

    for article in results[:5]:

        print(
            f"[{article['source']}] "
            f"{article['title']}"
        )