import sqlite3
import json
from datetime import datetime, timezone, timedelta

DB_PATH = "data/cache.db"
CACHE_EXPIRY_MINUTES = 30

def get_connection():
    """create and return a database connection"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # lets you access columns by name
    return conn

def init_db():
    """create tables if they don't exist yet"""
    conn = get_connection()
    cursor = conn.cursor()

    # table 1: cache news articles per topic
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS news_cache (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            topic TEXT NOT NULL,
            articles TEXT NOT NULL,      -- stored as JSON string
            fetched_at TEXT NOT NULL     -- ISO timestamp
        )
    """)

    # table 2: log every search made
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS search_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            topic TEXT NOT NULL,
            searched_at TEXT NOT NULL,
            result_count INTEGER
        )
    """)

    conn.commit()
    conn.close()
    print("Database initialized successfully")

def save_articles(topic, articles):
    """save fetched articles to cache"""
    conn = get_connection()
    cursor = conn.cursor()

    now = datetime.now(timezone.utc).isoformat()

    # delete old cache for this topic first
    cursor.execute("DELETE FROM news_cache WHERE topic = ?", (topic,))

    # insert fresh data
    cursor.execute("""
        INSERT INTO news_cache (topic, articles, fetched_at)
        VALUES (?, ?, ?)
    """, (topic, json.dumps(articles), now))

    conn.commit()
    conn.close()

def get_cached_articles(topic):
    """
    return cached articles if they exist and are fresh.
    returns None if cache is missing or expired.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT articles, fetched_at
        FROM news_cache
        WHERE topic = ?
        ORDER BY fetched_at DESC
        LIMIT 1
    """, (topic,))

    row = cursor.fetchone()
    conn.close()

    if not row:
        return None  # nothing cached

    # check if cache is still fresh
    fetched_at = datetime.fromisoformat(row["fetched_at"])
    age = datetime.now(timezone.utc) - fetched_at
    if age > timedelta(minutes=CACHE_EXPIRY_MINUTES):
        return None  # cache expired

    return json.loads(row["articles"])

def log_search(topic, result_count):
    """log every search for analytics"""
    conn = get_connection()
    cursor = conn.cursor()

    now = datetime.now(timezone.utc).isoformat()
    cursor.execute("""
        INSERT INTO search_log (topic, searched_at, result_count)
        VALUES (?, ?, ?)
    """, (topic, now, result_count))

    conn.commit()
    conn.close()

def get_popular_topics(limit=5):
    """return most searched topics — useful for dashboard"""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT topic, COUNT(*) as search_count
        FROM search_log
        GROUP BY topic
        ORDER BY search_count DESC
        LIMIT ?
    """, (limit,))

    rows = cursor.fetchall()
    conn.close()

    return [{"topic": row["topic"], "searches": row["search_count"]} for row in rows]

if __name__ == "__main__":
    init_db()

    # test save and retrieve
    test_articles = [
        {"title": "AI test article", "description": "test", "url": "", "source": "Test", "publishedAt": "2026-08-19T10:00:00Z"}
    ]

    save_articles("AI", test_articles)
    print("Saved articles for AI")

    cached = get_cached_articles("AI")
    print(f"Retrieved from cache: {len(cached)} articles")

    log_search("AI", len(cached))
    popular = get_popular_topics()
    print(f"Popular topics: {popular}")