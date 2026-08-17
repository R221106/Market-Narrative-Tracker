import nltk
from collections import Counter
from nltk.tokenize import word_tokenize

# download required nltk data — only runs once
nltk.download("punkt")
nltk.download("punkt_tab")
nltk.download("stopwords")

from nltk.corpus import stopwords

# base english stopwords
STOP_WORDS = set(stopwords.words("english"))

# add your own market-specific noise words
CUSTOM_NOISE = {
    "says", "said", "new", "one", "two", "three", "could", "would",
    "also", "may", "will", "get", "got", "like", "just", "make",
    "made", "know", "take", "year", "years", "time", "way", "us",
    "u", "s", "dont", "cant", "its", "thats", "heres", "whats",
    "reuters", "bloomberg", "cnn", "wsj", "ft", "article", "read",
    "news", "report", "according", "first", "last", "much", "many"
}

ALL_STOP_WORDS = STOP_WORDS | CUSTOM_NOISE

def extract_keywords(articles, top_n=10):
    if not articles:
        return []

    # collect all words from titles only (titles are most signal-rich)
    all_words = []
    for article in articles:
        title = article.get("title", "") or ""
        description = article.get("description", "") or ""

        # combine title and description
        text = f"{title} {description}".lower()

        # tokenize — splits into individual words
        tokens = word_tokenize(text)

        # filter: keep only real words, remove stopwords and short words
        filtered = [
            word for word in tokens
            if word.isalpha()           # letters only, no punctuation
            and len(word) > 2           # no 1-2 letter words
            and word not in ALL_STOP_WORDS  # not a noise word
        ]

        all_words.extend(filtered)

    # count and return top N
    counter = Counter(all_words)
    top_keywords = counter.most_common(top_n)

    # format as list of dicts
    return [
        {"word": word, "count": count}
        for word, count in top_keywords
    ]

if __name__ == "__main__":
    # test with fake articles
    test_articles = [
        {"title": "AI chip demand surges as Nvidia reports record revenue", "description": "Nvidia posted record earnings driven by AI chip demand from data centers"},
        {"title": "OpenAI raises funding amid AI regulation concerns", "description": "Regulators push for stricter AI oversight as investment continues"},
        {"title": "AI powers new wave of market automation tools", "description": "Wall Street firms adopt AI automation for trading and analytics"},
        {"title": "Nvidia GPU shortage hits AI startups hard", "description": "Small AI companies struggle to access Nvidia chips amid shortage"},
        {"title": "AI regulation bill passes Senate committee", "description": "New legislation targets AI safety and transparency requirements"}
    ]

    keywords = extract_keywords(test_articles, top_n=10)
    print("=== Top Keywords ===\n")
    for kw in keywords:
        print(f"{kw['word']:<20} count: {kw['count']}")