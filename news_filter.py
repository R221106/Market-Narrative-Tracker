# ============================================================
# MARKET RELEVANCE FILTER
# ============================================================


# ============================================================
# MARKET KEYWORDS
# ============================================================

MARKET_KEYWORDS = [

    "market",
    "markets",
    "stock",
    "stocks",
    "share",
    "shares",

    "investor",
    "investors",
    "investment",
    "investments",

    "revenue",
    "earnings",
    "profit",
    "profits",
    "loss",
    "valuation",

    "company",
    "companies",
    "industry",
    "industries",

    "demand",
    "growth",
    "sales",

    "funding",
    "acquisition",
    "merger",

    "regulation",
    "regulatory",

    "tariff",
    "tariffs",

    "export",
    "exports",

    "supply chain",

    "economic",
    "economy",
    "business",

    "forecast",
    "outlook",

    "spending",
    "capital",
    "venture",
    "startup"
]


# ============================================================
# OBVIOUSLY IRRELEVANT TOPICS
# ============================================================

EXCLUDED_KEYWORDS = [

    # Sports
    "wnba",
    "nba",
    "nfl",
    "mlb",
    "nhl",
    "football",
    "basketball",
    "baseball",
    "soccer",
    "tennis",
    "cricket",
    "rugby",
    "golf",

    "match",
    "matches",
    "game",
    "games",
    "player",
    "players",
    "coach",
    "coaching",

    "score",
    "scores",
    "scored",

    "recruiting",
    "recruitment",

    # Entertainment
    "bollywood",
    "hollywood",
    "actress",
    "actor",
    "celebrity",
    "celebrities",

    "fashion",
    "saree",
    "red carpet",

    "reality tv",

    # Lifestyle
    "recipe",
    "recipes",
    "cooking",
    "travel",
    "vacation",
    "horoscope",
    "wedding",

    # Other obvious noise
    "eagle viewing",
    "field trip"
]


# ============================================================
# NARRATIVE KEYWORDS
# ============================================================

NARRATIVE_KEYWORDS = {

    "AI": [

        "artificial intelligence",
        "ai",

        "machine learning",
        "generative ai",

        "large language model",
        "llm",

        "chatbot",

        "openai",
        "anthropic",
        "gemini",

        "nvidia",

        "gpu",
        "gpus",

        "data center",
        "data centres",

        "ai infrastructure",

        "ai chip",
        "ai chips",

        "semiconductor",
        "semiconductors"
    ],


    "EV": [

        "electric vehicle",
        "electric vehicles",

        "ev",
        "evs",

        "battery",
        "batteries",

        "charging",

        "tesla",
        "byd",

        "automotive",
        "automaker",
        "automakers",

        "electric car",
        "electric cars"
    ],


    "Quantum Computing": [

        "quantum computing",
        "quantum computer",
        "quantum computers",

        "quantum technology",

        "quantum chip",
        "quantum processor",

        "quantum computing industry"
    ],


    "Semiconductors": [

        "semiconductor",
        "semiconductors",

        "chip",
        "chips",

        "microchip",
        "processor",

        "gpu",
        "gpus",

        "cpu",
        "cpus",

        "foundry",

        "tsmc",
        "intel",
        "amd",
        "nvidia"
    ]
}


# ============================================================
# TEXT
# ============================================================

def get_article_text(article):

    title = article.get("title") or ""
    description = article.get("description") or ""
    content = article.get("content") or ""

    return (
        f"{title} {description} {content}"
    ).lower()


# ============================================================
# EXCLUSION
# ============================================================

def contains_excluded_keyword(article):

    text = get_article_text(article)

    for keyword in EXCLUDED_KEYWORDS:

        if keyword.lower() in text:
            return True

    return False


# ============================================================
# NARRATIVE MATCHES
# ============================================================

def get_narrative_matches(article, narrative):

    text = get_article_text(article)

    keywords = NARRATIVE_KEYWORDS.get(
        narrative,
        []
    )

    matches = []

    for keyword in keywords:

        if keyword.lower() in text:
            matches.append(keyword)

    return matches


# ============================================================
# MARKET MATCHES
# ============================================================

def get_market_matches(article):

    text = get_article_text(article)

    matches = []

    for keyword in MARKET_KEYWORDS:

        if keyword.lower() in text:
            matches.append(keyword)

    return matches


# ============================================================
# RELEVANCE SCORE
# ============================================================

def calculate_relevance_score(
    article,
    narrative
):

    narrative_matches = get_narrative_matches(
        article,
        narrative
    )

    market_matches = get_market_matches(
        article
    )

    title = (
        article.get("title") or ""
    ).lower()

    score = 0

    # Narrative relevance
    score += len(narrative_matches) * 3

    # Market/business relevance
    score += len(market_matches)

    # Extra importance if narrative appears in title
    for keyword in narrative_matches:

        if keyword.lower() in title:

            score += 3

    return score


# ============================================================
# FILTER
# ============================================================

def filter_articles(
    articles,
    narrative,
    minimum_score=5
):

    filtered_articles = []

    for article in articles:

        # --------------------------------------------
        # Remove obvious irrelevant content
        # --------------------------------------------

        if contains_excluded_keyword(article):
            continue

        # --------------------------------------------
        # Calculate relevance
        # --------------------------------------------

        score = calculate_relevance_score(
            article,
            narrative
        )

        # --------------------------------------------
        # Remove low relevance articles
        # --------------------------------------------

        if score < minimum_score:
            continue

        # --------------------------------------------
        # Add filtering information
        # --------------------------------------------

        article["relevance_score"] = score

        article["narrative_matches"] = (
            get_narrative_matches(
                article,
                narrative
            )
        )

        article["market_matches"] = (
            get_market_matches(article)
        )

        filtered_articles.append(article)

    # Highest relevance first
    filtered_articles.sort(
        key=lambda article: article["relevance_score"],
        reverse=True
    )

    return filtered_articles