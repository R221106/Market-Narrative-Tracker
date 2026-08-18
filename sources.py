from collections import Counter

def analyze_sources(articles, top_n=8):
    if not articles:
        return []

    # count articles per source
    source_counts = Counter()

    for article in articles:
        source = article.get("source", "Unknown")
        if source and source != "Unknown":
            source_counts[source] += 1

    # get top N sources
    top_sources = source_counts.most_common(top_n)

    total = sum(source_counts.values())

    return [
        {
            "source": source,
            "count": count,
            # percentage share of total coverage
            "share": round((count / total) * 100, 1)
        }
        for source, count in top_sources
    ]

if __name__ == "__main__":
    test_articles = [
        {"source": "Reuters"},
        {"source": "Reuters"},
        {"source": "Reuters"},
        {"source": "Bloomberg"},
        {"source": "Bloomberg"},
        {"source": "CNN"},
        {"source": "BBC"},
        {"source": "BBC"},
        {"source": "The Guardian"},
        {"source": "Unknown"},
    ]

    results = analyze_sources(test_articles)
    print("=== Top Sources ===\n")
    for s in results:
        bar = "█" * s["count"]
        print(f"{s['source']:<20} {bar:<10} {s['count']} articles ({s['share']}%)")