import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("NEWS_API_KEY")
BASE_URL = "https://newsapi.org/v2/everything"


def fetch_news(topic):
    params = {
        "q": topic,
        "language": "en",
        "sortBy": "publishedAt",
        "pageSize": 10,
        "apiKey": API_KEY
    }

    response = requests.get(
        BASE_URL,
        params=params,
        timeout=5
    )

    print("Status code:", response.status_code)

    data = response.json()

    articles = data.get("articles", [])

    print("Number of articles:", len(articles))

    for article in articles[:5]:
        print(article.get("title", "No title"))

    return articles


if __name__ == "__main__":
    fetch_news("Artificial Intelligence")