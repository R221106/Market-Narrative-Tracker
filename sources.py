from collections import Counter

from config import TOP_SOURCES_COUNT


def analyze_sources(
    articles,
    top_n=TOP_SOURCES_COUNT
):

    if not articles:
        return []

    source_counts = Counter(
        article.get("source", "Unknown")
        for article in articles
        if article.get("source")
        and article.get("source") != "Unknown"
    )

    total = sum(source_counts.values())

    if total == 0:
        return []

    top_sources = source_counts.most_common(top_n)

    results = [
        {
            "source": source,
            "count": count,
            "share": round((count / total) * 100, 1)
        }
        for source, count in top_sources
    ]

    top_count = sum(count for _, count in top_sources)
    other_count = total - top_count

    if other_count > 0:
        results.append({
            "source": "Other",
            "count": other_count,
            "share": round((other_count / total) * 100, 1)
        })

    return results