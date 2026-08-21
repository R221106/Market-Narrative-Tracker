from datetime import datetime

from collections import defaultdict

from config import (
    TREND_RISING_THRESHOLD,
    TREND_DECLINING_THRESHOLD
)


def analyze_trend(articles, topic):

    if not articles:

        return {
            "topic": topic,
            "trend": "insufficient data",
            "velocity": 0,
            "total_articles": 0,
            "buckets": []
        }

    hourly_buckets = defaultdict(int)

    for article in articles:

        published = article.get(
            "publishedAt",
            ""
        )

        if not published:
            continue

        try:

            dt = datetime.strptime(
                published,
                "%Y-%m-%dT%H:%M:%SZ"
            )

            hour = dt.strftime(
                "%Y-%m-%d %H:00"
            )

            hourly_buckets[hour] += 1

        except ValueError:

            continue

    sorted_buckets = sorted(
        hourly_buckets.items()
    )

    trend_label, velocity = (
        _calculate_velocity(
            sorted_buckets
        )
    )

    return {

        "topic": topic,

        "trend": trend_label,

        "velocity": velocity,

        "total_articles": len(articles),

        "buckets": [

            {
                "hour": hour,
                "count": count
            }

            for hour, count in sorted_buckets
        ]
    }


def _calculate_velocity(sorted_buckets):

    if len(sorted_buckets) < 2:

        return "stable", 0

    mid = len(sorted_buckets) // 2

    first_half = sum(
        count
        for _, count in sorted_buckets[:mid]
    )

    second_half = sum(
        count
        for _, count in sorted_buckets[mid:]
    )

    if first_half == 0:

        velocity = 100.0

    else:

        velocity = round(
            (
                (second_half - first_half)
                / first_half
            ) * 100,
            1
        )

    if velocity >= TREND_RISING_THRESHOLD:

        label = "rising"

    elif velocity <= TREND_DECLINING_THRESHOLD:

        label = "declining"

    else:

        label = "stable"

    return label, velocity