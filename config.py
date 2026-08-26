import os
import re
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
# GNEWS API                          ← ADD THIS SECTION
# ============================================================

GNEWS_API_KEY = os.getenv("GNEWS_API_KEY")
GNEWS_BASE_URL = "https://gnews.io/api/v4/search"
GNEWS_MAX_RESULTS = 10


# ============================================================
# ANTHROPIC API                      ← ADD THIS SECTION
# ============================================================

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")


# ============================================================
# DATABASE / CACHE
# ============================================================

IS_PRODUCTION = os.getenv("RENDER", False)          # ← ADD THIS LINE
DB_PATH = "/tmp/cache.db" if IS_PRODUCTION else "data/cache.db"  # ← REPLACE DB_PATH
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


# ============================================================
# INPUT VALIDATION                   ← ADD THIS SECTION
# ============================================================

MAX_TOPIC_LENGTH = 100

def sanitize_topic(topic):
    """remove special characters, limit length"""
    cleaned = re.sub(r'[^\w\s-]', '', topic)
    return cleaned.strip()[:MAX_TOPIC_LENGTH]