import os
from dotenv import load_dotenv

load_dotenv()


# ============================================================
# NEWS API
# ============================================================

NEWS_API_KEY = os.getenv("NEWS_API_KEY")

NEWS_API_BASE_URL = "https://newsapi.org/v2/everything"

NEWS_API_PAGE_SIZE = 10

NEWS_API_TIMEOUT = 5


# ============================================================
# DATABASE / CACHE
# ============================================================

DB_PATH = "data/cache.db"

CACHE_EXPIRY_MINUTES = 30


# ============================================================
# DEFAULT TOPICS
# ============================================================

DEFAULT_TOPIC = "AI"

WATCHLIST_TOPICS = [
    "AI",
    "Nvidia",
    "Bitcoin",
    "Oil",
    "Tesla",
    "EVs",
    "Quantum Computing",
    "Crypto",
    "Fed",
    "Inflation"
]


# ============================================================
# SENTIMENT
# ============================================================

SENTIMENT_POSITIVE_THRESHOLD = 0.05

SENTIMENT_NEGATIVE_THRESHOLD = -0.05


# ============================================================
# TREND
# ============================================================

TREND_RISING_THRESHOLD = 30

TREND_DECLINING_THRESHOLD = -30


# ============================================================
# ANALYTICS
# ============================================================

TOP_KEYWORDS_COUNT = 10

TOP_SOURCES_COUNT = 8

