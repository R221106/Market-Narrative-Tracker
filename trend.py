from datetime import datetime, timezone
from collections import defaultdict

def analyze_trend(articles, topic):
    if not articles:
        return {
            "topic": topic,
            "trend": "insufficient data",
            "velocity": 0,
            "buckets": []
        }

    # group articles by hour using publishedAt timestamp
    hourly_buckets = defaultdict(int)

    for article in articles:
        published = article.get("publishedAt", "")
        if not published:
            continue
        try:
            # parse ISO timestamp e.g. "2026-08-18T09:25:11Z"
            dt = datetime.strptime(published, "%Y-%m-%dT%H:%M:%SZ")
            # round down to the hour
            hour_key = dt.strftime("%Y-%m-%d %H:00")
            hourly_buckets[hour_key] += 1
        except ValueError:
            continue

    # sort buckets chronologically
    sorted_buckets = sorted(hourly_buckets.items())

    if len(sorted_buckets) < 2:
        trend_label = "stable"
        velocity = 0
    else:
        # split into first half and second half
        mid = len(sorted_buckets) // 2
        first_half = sum(count for _, count in sorted_buckets[:mid])
        second_half = sum(count for _, count in sorted_buckets[mid:])

        # velocity = how much it changed
        if first_half == 0:
            velocity = 100  # went from nothing to something = big spike
        else:
            velocity = round(((second_half - first_half) / first_half) * 100, 1)

        # label the trend
        if velocity >= 30:
            trend_label = "rising"
        elif velocity <= -30:
            trend_label = "declining"
        else:
            trend_label = "stable"

    return {
        "topic": topic,
        "trend": trend_label,
        "velocity": velocity,       # % change, e.g. 45.5 means 45.5% more articles recently
        "total_articles": len(articles),
        "buckets": [
            {"hour": hour, "count": count}
            for hour, count in sorted_buckets
        ]
    }

if __name__ == "__main__":
    # test with fake articles spread across hours
    test_articles = [
        {"publishedAt": "2026-08-18T06:00:00Z"},
        {"publishedAt": "2026-08-18T07:00:00Z"},
        {"publishedAt": "2026-08-18T07:30:00Z"},
        {"publishedAt": "2026-08-18T09:00:00Z"},
        {"publishedAt": "2026-08-18T09:15:00Z"},
        {"publishedAt": "2026-08-18T09:45:00Z"},
        {"publishedAt": "2026-08-18T10:00:00Z"},
        {"publishedAt": "2026-08-18T10:30:00Z"},
    ]

    result = analyze_trend(test_articles, "AI")
    print(f"Trend:    {result['trend']}")
    print(f"Velocity: {result['velocity']}%")
    print(f"\nHourly breakdown:")
    for bucket in result["buckets"]:
        bar = "█" * bucket["count"]
        print(f"  {bucket['hour']}  {bar} ({bucket['count']})")