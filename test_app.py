import pytest
import json
from app import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

# ── HOME ROUTE ──────────────────────────────────────────

def test_home_returns_200(client):
    """home route should be reachable"""
    response = client.get("/")
    assert response.status_code == 200

# ── /api/news ───────────────────────────────────────────

def test_news_returns_200(client):
    """news route should return 200 with a valid topic"""
    response = client.get("/api/news?topic=AI")
    assert response.status_code == 200

def test_news_response_has_correct_keys(client):
    """news response must have topic and articles keys"""
    response = client.get("/api/news?topic=AI")
    data = json.loads(response.data)
    assert "topic" in data
    assert "articles" in data

def test_news_articles_is_a_list(client):
    """articles must always be a list, never null"""
    response = client.get("/api/news?topic=AI")
    data = json.loads(response.data)
    assert isinstance(data["articles"], list)

def test_news_article_fields(client):
    """each article must have the 5 required fields"""
    response = client.get("/api/news?topic=AI")
    data = json.loads(response.data)
    if data["articles"]:  # only check if articles exist
        first = data["articles"][0]
        assert "title" in first
        assert "description" in first
        assert "url" in first
        assert "source" in first
        assert "publishedAt" in first

def test_news_empty_topic_returns_400(client):
    """empty topic must return 400 error"""
    response = client.get("/api/news?topic=")
    assert response.status_code == 400

def test_news_default_topic_is_ai(client):
    """missing topic param should default to AI"""
    response = client.get("/api/news")
    data = json.loads(response.data)
    assert response.status_code == 200
    assert data["topic"] == "AI"

# ── /api/sentiment ──────────────────────────────────────

def test_sentiment_returns_200(client):
    """sentiment route should return 200"""
    response = client.get("/api/sentiment?topic=AI")
    assert response.status_code == 200

def test_sentiment_has_correct_keys(client):
    """sentiment response must have topic, overall, articles"""
    response = client.get("/api/sentiment?topic=AI")
    data = json.loads(response.data)
    assert "topic" in data
    assert "overall" in data
    assert "articles" in data

def test_sentiment_overall_has_label_and_score(client):
    """overall sentiment must have label and score"""
    response = client.get("/api/sentiment?topic=AI")
    data = json.loads(response.data)
    overall = data["overall"]
    assert "label" in overall
    assert "score" in overall

def test_sentiment_label_is_valid(client):
    """sentiment label must be positive, negative, or neutral"""
    response = client.get("/api/sentiment?topic=AI")
    data = json.loads(response.data)
    assert data["overall"]["label"] in ["positive", "negative", "neutral"]

def test_sentiment_score_is_in_range(client):
    """compound score must be between -1 and 1"""
    response = client.get("/api/sentiment?topic=AI")
    data = json.loads(response.data)
    score = data["overall"]["score"]
    assert -1.0 <= score <= 1.0

def test_sentiment_articles_sorted_by_score(client):
    """articles must be sorted highest score first"""
    response = client.get("/api/sentiment?topic=AI")
    data = json.loads(response.data)
    articles = data["articles"]
    if len(articles) > 1:
        scores = [a["score"] for a in articles]
        assert scores == sorted(scores, reverse=True)

def test_sentiment_empty_topic_returns_400(client):
    """empty topic must return 400"""
    response = client.get("/api/sentiment?topic=")
    assert response.status_code == 400

# ── /api/keywords ───────────────────────────────────────

def test_keywords_returns_200(client):
    """keywords route should return 200"""
    response = client.get("/api/keywords?topic=AI")
    assert response.status_code == 200

def test_keywords_has_correct_keys(client):
    """keywords response must have topic, count, keywords"""
    response = client.get("/api/keywords?topic=AI")
    data = json.loads(response.data)
    assert "topic" in data
    assert "count" in data
    assert "keywords" in data

def test_keywords_each_item_has_word_and_count(client):
    """each keyword must have word and count fields"""
    response = client.get("/api/keywords?topic=AI")
    data = json.loads(response.data)
    if data["keywords"]:
        first = data["keywords"][0]
        assert "word" in first
        assert "count" in first

def test_keywords_no_stopwords(client):
    """common stopwords must not appear in results"""
    response = client.get("/api/keywords?topic=AI")
    data = json.loads(response.data)
    words = [kw["word"] for kw in data["keywords"]]
    stopwords_to_check = ["the", "and", "is", "are", "was", "said", "says"]
    for stopword in stopwords_to_check:
        assert stopword not in words

def test_keywords_empty_topic_returns_400(client):
    """empty topic must return 400"""
    response = client.get("/api/keywords?topic=")
    assert response.status_code == 400

# ── /api/trend ──────────────────────────────────────────

def test_trend_returns_200(client):
    """trend route should return 200"""
    response = client.get("/api/trend?topic=AI")
    assert response.status_code == 200

def test_trend_has_correct_keys(client):
    """trend response must have required keys"""
    response = client.get("/api/trend?topic=AI")
    data = json.loads(response.data)
    assert "topic" in data
    assert "trend" in data
    assert "velocity" in data
    assert "buckets" in data

def test_trend_label_is_valid(client):
    """trend label must be rising, stable, or declining"""
    response = client.get("/api/trend?topic=AI")
    data = json.loads(response.data)
    assert data["trend"] in ["rising", "stable", "declining", "insufficient data"]

def test_trend_empty_topic_returns_400(client):
    """empty topic must return 400"""
    response = client.get("/api/trend?topic=")
    assert response.status_code == 400

# ── /api/sources ────────────────────────────────────────

def test_sources_returns_200(client):
    """sources route should return 200"""
    response = client.get("/api/sources?topic=AI")
    assert response.status_code == 200

def test_sources_has_correct_keys(client):
    """sources response must have topic and sources"""
    response = client.get("/api/sources?topic=AI")
    data = json.loads(response.data)
    assert "topic" in data
    assert "sources" in data

def test_sources_each_item_has_required_fields(client):
    """each source must have source, count, share"""
    response = client.get("/api/sources?topic=AI")
    data = json.loads(response.data)
    if data["sources"]:
        first = data["sources"][0]
        assert "source" in first
        assert "count" in first
        assert "share" in first

def test_sources_share_adds_to_100(client):
    """all source shares must add up to ~100%"""
    response = client.get("/api/sources?topic=AI")
    data = json.loads(response.data)
    if data["sources"]:
        total_share = sum(s["share"] for s in data["sources"])
        # allow small rounding error
        assert 95.0 <= total_share <= 100.0

def test_sources_empty_topic_returns_400(client):
    """empty topic must return 400"""
    response = client.get("/api/sources?topic=")
    assert response.status_code == 400