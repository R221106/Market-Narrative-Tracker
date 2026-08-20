import nltk

from collections import Counter

from nltk.tokenize import word_tokenize

from nltk.corpus import stopwords

from config import TOP_KEYWORDS_COUNT


# ============================================================
# NLTK DATA
# ============================================================

nltk.download("punkt", quiet=True)

nltk.download("punkt_tab", quiet=True)

nltk.download("stopwords", quiet=True)


# ============================================================
# CUSTOM NOISE WORDS
# ============================================================

CUSTOM_NOISE = {

    "says",
    "said",
    "new",
    "one",
    "two",
    "three",

    "could",
    "would",
    "also",
    "may",
    "will",

    "get",
    "got",
    "like",
    "just",
    "make",
    "made",

    "know",
    "take",

    "year",
    "years",
    "time",
    "way",

    "us",
    "u",
    "s",

    "dont",
    "cant",
    "its",
    "thats",
    "heres",
    "whats",

    "reuters",
    "bloomberg",
    "cnn",
    "wsj",
    "ft",

    "article",
    "read",
    "news",
    "report",
    "according",

    "first",
    "last",
    "much",
    "many"
}


# ============================================================
# ALL STOP WORDS
# ============================================================

ALL_STOP_WORDS = (
    set(stopwords.words("english"))
    | CUSTOM_NOISE
)


# ============================================================
# KEYWORD EXTRACTION
# ============================================================

def extract_keywords(
    articles,
    top_n=TOP_KEYWORDS_COUNT
):
    """
    Extract the most common meaningful words
    from article titles and descriptions.
    """

    if not articles:

        return []

    all_words = []

    for article in articles:

        title = article.get(
            "title",
            ""
        ) or ""

        description = article.get(
            "description",
            ""
        ) or ""

        text = (
            f"{title} {description}"
        ).lower()

        tokens = word_tokenize(text)

        filtered = [

            word

            for word in tokens

            if word.isalpha()

            and len(word) > 2

            and word not in ALL_STOP_WORDS
        ]

        all_words.extend(filtered)

    counter = Counter(all_words)

    top_keywords = counter.most_common(
        top_n
    )

    return [

        {
            "word": word,
            "count": count
        }

        for word, count in top_keywords
    ]