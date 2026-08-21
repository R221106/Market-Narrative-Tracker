from collections import Counter

from config import TOP_SOURCES_COUNT


def analyze_sources(
    articles,
    top_n=TOP_SOURCES_COUNT
):

    if not articles:

        return []

    source_counts = Counter(

        article.get(
            "source",
            "Unknown"
        )

        for article in articles

        if article.get("source")
        and article.get("source") != "Unknown"
    )

    total = sum(
        source_counts.values()
    )

    if total == 0:

        return []

    return [

        {
            "source": source,

            "count": count,

            "share": round(
                (count / total) * 100,
                1
            )
        }

        for source, count
        in source_counts.most_common(top_n)
    ]