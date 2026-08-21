import os

from dotenv import load_dotenv
from google import genai


# ============================================================
# ENVIRONMENT
# ============================================================

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


# ============================================================
# GEMINI CLIENT
# ============================================================

if not GEMINI_API_KEY:
    print("Warning: GEMINI_API_KEY not found in .env")

    client = None

else:
    client = genai.Client(
        api_key=GEMINI_API_KEY
    )


# ============================================================
# SUMMARY GENERATOR
# ============================================================

def generate_summary(
    topic,
    articles,
    sentiment_label,
    top_keywords
):
    """
    Generate an AI-powered market narrative summary.

    Parameters:
        topic: The market topic being analysed.
        articles: List of news articles.
        sentiment_label: Overall sentiment label.
        top_keywords: Most important keywords.

    Returns:
        A generated summary string.
    """

    # --------------------------------------------------------
    # Check API configuration
    # --------------------------------------------------------

    if client is None:

        return (
            f"Summary unavailable for '{topic}' "
            "because GEMINI_API_KEY is not configured."
        )


    # --------------------------------------------------------
    # Prepare article information
    # --------------------------------------------------------

    article_text = ""

    # Only send the first 10 articles.
    # This keeps the API request small and efficient.

    for article in articles[:10]:

        title = article.get(
            "title",
            ""
        )

        description = article.get(
            "description",
            ""
        )

        source = article.get(
            "source",
            {}
        )

        # NewsAPI normally returns source as a dictionary.
        # Example:
        # {"id": null, "name": "BBC News"}

        if isinstance(source, dict):

            source_name = source.get(
                "name",
                "Unknown source"
            )

        else:

            source_name = str(source)


        article_text += f"""
Title: {title}
Source: {source_name}
Description: {description}

"""


    # --------------------------------------------------------
    # Prepare keywords
    # --------------------------------------------------------

    keyword_text = ""

    for keyword in top_keywords:

        # Your keywords are expected to look like:
        #
        # {"word": "AI", "count": 15}
        #
        # But this also handles plain strings.

        if isinstance(keyword, dict):

            word = keyword.get(
                "word",
                ""
            )

        else:

            word = str(keyword)

        if word:

            keyword_text += f"- {word}\n"


    # --------------------------------------------------------
    # Create prompt
    # --------------------------------------------------------

    prompt = f"""
You are a financial market analyst helping analyse
current market narratives.

Your task is to produce a concise, objective summary
of the current news narrative surrounding the topic:

TOPIC:
{topic}

OVERALL SENTIMENT:
{sentiment_label}

TOP KEYWORDS:
{keyword_text}

RECENT NEWS ARTICLES:
{article_text}

Write a clear market narrative summary.

The summary should:

1. Explain what is currently happening around the topic.
2. Identify the main themes appearing across the news.
3. Mention important developments or events.
4. Explain whether the overall narrative appears
   positive, negative, or mixed.
5. Be based ONLY on the information provided in
   the articles.
6. Avoid making up facts.
7. Do not give investment or financial advice.

Keep the summary to approximately 2-3 short paragraphs.

Do not use headings such as "Summary" or "Analysis".
Just provide the final narrative.
"""


    # --------------------------------------------------------
    # Call Gemini
    # --------------------------------------------------------

    try:

        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt,
            config={
                "automatic_function_calling": {
                "disable": True
                }
            }
        )

        # Gemini returns the generated text here.

        if response.text:

            return response.text.strip()

        else:

            return (
                f"Summary unavailable for '{topic}' "
                "because Gemini returned no text."
            )


    # --------------------------------------------------------
    # Handle API errors
    # --------------------------------------------------------

    except Exception as e:

        print(
            f"Gemini API error: {e}"
        )

        return (
            f"Summary unavailable for '{topic}' "
            "at this time."
        )


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    print()
    print("=" * 60)
    print("Gemini Summariser")
    print("=" * 60)
    print()

    # Simple test articles

    test_articles = [

        {
            "title": "AI investment continues to grow",
            "description":
                "Technology companies continue to invest "
                "heavily in artificial intelligence."
        },

        {
            "title": "Nvidia benefits from AI demand",
            "description":
                "Demand for AI chips remains strong "
                "as companies expand their AI infrastructure."
        },

        {
            "title": "Investors watch AI valuations",
            "description":
                "Investors are increasingly monitoring "
                "the valuations of companies exposed to AI."
        }

    ]


    # Test keywords

    test_keywords = [

        {
            "word": "AI",
            "count": 20
        },

        {
            "word": "Nvidia",
            "count": 12
        },

        {
            "word": "investment",
            "count": 10
        },

        {
            "word": "chips",
            "count": 8
        },

        {
            "word": "technology",
            "count": 7
        }

    ]


    # Generate summary

    summary = generate_summary(

        topic="AI",

        articles=test_articles,

        sentiment_label="Positive",

        top_keywords=test_keywords

    )


    print("=== Generated Summary ===")
    print()
    print(summary)
    print()
    print("=" * 60)