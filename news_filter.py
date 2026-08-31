from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re

# ============================================================
# EXCLUSION LIST — sports/lifestyle noise
# only need this small list now
# ============================================================

EXCLUDED_KEYWORDS = [
    "wnba", "nba", "nfl", "mlb", "nhl",
    "football", "basketball", "baseball",
    "soccer", "tennis", "cricket", "rugby",
    "bollywood", "hollywood", "actress", "actor",
    "celebrity", "recipe", "cooking", "horoscope",
    "wedding", "fashion", "travel", "vacation"
]

def contains_excluded_keyword(article):
    title = (article.get("title") or "").lower()
    for keyword in EXCLUDED_KEYWORDS:
        pattern = r"\b" + re.escape(keyword) + r"\b"
        if re.search(pattern, title):
            return True
    return False

def get_article_text(article):
    title       = article.get("title", "") or ""
    description = article.get("description", "") or ""
    content     = article.get("content", "") or ""
    # title weighted more by repeating it
    return f"{title} {title} {description} {content}"

def filter_articles(articles, narrative, minimum_score=0.05):
    """
    Score articles by cosine similarity to the topic.
    No hardcoded keyword lists needed.
    minimum_score: 0.0 to 1.0 — how similar it must be
    """
    if not articles:
        return []

    # remove obvious noise first
    candidates = [
        a for a in articles
        if not contains_excluded_keyword(a)
    ]

    if not candidates:
        return []

    # build text for each article
    article_texts = [get_article_text(a) for a in candidates]

    # the topic itself is the reference document
    all_texts = [narrative] + article_texts

    # TF-IDF vectorizer — converts text to numbers
    vectorizer = TfidfVectorizer(
        stop_words="english",
        ngram_range=(1, 2),   # single words AND two-word phrases
        min_df=1
    )

    try:
        tfidf_matrix = vectorizer.fit_transform(all_texts)
    except ValueError:
        # fallback if vectorizer fails
        return candidates

    # cosine similarity between topic (row 0) and each article
    topic_vector   = tfidf_matrix[0]
    article_matrix = tfidf_matrix[1:]

    similarities = cosine_similarity(
        topic_vector, article_matrix
    ).flatten()

    # attach scores and filter
    scored = []
    for i, article in enumerate(candidates):
        score = round(float(similarities[i]), 4)
        if score >= minimum_score:
            article["relevance_score"] = score
            scored.append(article)

    # highest similarity first
    scored.sort(
        key=lambda a: a["relevance_score"],
        reverse=True
    )

    return scored
