# Market Narrative Tracker — API Documentation

Base URL: `http://127.0.0.1:5000`

All endpoints return JSON. All endpoints accept GET requests only.

---

## Table of Contents
- [GET /](#get-)
- [GET /api/news](#get-apinews)
- [GET /api/sentiment](#get-apisentiment)
- [GET /api/keywords](#get-apikeywords)
- [GET /api/trend](#get-apitrend)
- [GET /api/sources](#get-apisources)
- [GET /api/summary](#get-apisummary)
- [GET /api/topics](#get-apitopics)
- [GET /api/popular](#get-apipopular)
- [Error Responses](#error-responses)

---

## GET /

Health check. Confirms the server is running.

**Parameters:** none

**Example request:**
```
GET http://127.0.0.1:5000/
```

**Example response:**
```
Market Narrative Tracker — backend running
```

---

## GET /api/news

Fetches the latest news articles for a given market narrative topic.
Results are cached for 30 minutes — repeated calls within that window
are served from the local SQLite database.

**Parameters:**

| Parameter | Type   | Required | Default | Description |
|-----------|--------|----------|---------|-------------|
| topic     | string | No       | AI      | Market narrative to search for |

**Example request:**
```
GET http://127.0.0.1:5000/api/news?topic=Bitcoin
```

**Example response:**
```json
{
  "topic": "Bitcoin",
  "articles": [
    {
      "title": "Bitcoin surges past $100k amid ETF approval",
      "description": "Bitcoin reached a new all-time high following...",
      "url": "https://example.com/article",
      "source": "Reuters",
      "publishedAt": "2026-08-22T09:00:00Z"
    }
  ]
}
```

**Notes:**
- Returns up to 10 articles per request
- Articles sorted by most recently published
- Empty or whitespace topic returns 400

---

## GET /api/sentiment

Returns overall sentiment for a topic plus individual sentiment
scores for each article. Uses VADER with a custom financial
lexicon tuned for market terminology.

**Parameters:**

| Parameter | Type   | Required | Default | Description |
|-----------|--------|----------|---------|-------------|
| topic     | string | No       | AI      | Market narrative to analyse |

**Example request:**
```
GET http://127.0.0.1:5000/api/sentiment?topic=Tesla
```

**Example response:**
```json
{
  "topic": "Tesla",
  "overall": {
    "label": "positive",
    "score": 0.312
  },
  "articles": [
    {
      "title": "Tesla rally continues as EV sales beat expectations",
      "description": "Tesla reported record deliveries...",
      "url": "https://example.com/article",
      "source": "Bloomberg",
      "publishedAt": "2026-08-22T10:00:00Z",
      "sentiment": "positive",
      "score": 0.681
    },
    {
      "title": "Tesla faces regulatory scrutiny over autopilot",
      "description": "Federal regulators announced...",
      "url": "https://example.com/article2",
      "source": "CNN",
      "publishedAt": "2026-08-22T08:00:00Z",
      "sentiment": "negative",
      "score": -0.423
    }
  ]
}
```

**Notes:**
- `score` ranges from -1.0 (most negative) to +1.0 (most positive)
- `label` is one of: `positive`, `neutral`, `negative`
- Articles sorted by score descending — most positive first
- Scoring thresholds: positive ≥ 0.05, negative ≤ -0.05

---

## GET /api/keywords

Extracts the most frequently occurring meaningful words from
article headlines and descriptions for a given topic.
Filters out common English stopwords and market noise words.

**Parameters:**

| Parameter | Type   | Required | Default | Description |
|-----------|--------|----------|---------|-------------|
| topic     | string | No       | AI      | Market narrative to extract keywords from |

**Example request:**
```
GET http://127.0.0.1:5000/api/keywords?topic=AI
```

**Example response:**
```json
{
  "topic": "AI",
  "count": 10,
  "keywords": [
    { "word": "nvidia", "count": 4 },
    { "word": "chip", "count": 3 },
    { "word": "regulation", "count": 2 },
    { "word": "funding", "count": 2 },
    { "word": "model", "count": 1 }
  ]
}
```

**Notes:**
- Returns top 10 keywords by default
- `count` reflects frequency across all fetched articles
- Use `count` to scale font size in a tag cloud display
- Stopwords filtered: common English words + market noise (reuters, bloomberg, said, etc.)

---

## GET /api/trend

Analyses narrative momentum by grouping articles into hourly
buckets and comparing early vs recent volume to calculate
a velocity percentage.

**Parameters:**

| Parameter | Type   | Required | Default | Description |
|-----------|--------|----------|---------|-------------|
| topic     | string | No       | AI      | Market narrative to analyse trend for |

**Example request:**
```
GET http://127.0.0.1:5000/api/trend?topic=Nvidia
```

**Example response:**
```json
{
  "topic": "Nvidia",
  "trend": "rising",
  "velocity": 45.5,
  "total_articles": 10,
  "buckets": [
    { "hour": "2026-08-22 07:00", "count": 2 },
    { "hour": "2026-08-22 08:00", "count": 2 },
    { "hour": "2026-08-22 09:00", "count": 4 },
    { "hour": "2026-08-22 10:00", "count": 2 }
  ]
}
```

**Notes:**
- `trend` is one of: `rising`, `stable`, `declining`, `insufficient data`
- `velocity` is the % change between first and second half of the time window
- Thresholds: rising ≥ 30%, declining ≤ -30%
- `buckets` is the data array for a line chart — hour on x-axis, count on y-axis

---

## GET /api/sources

Returns the top publishers driving coverage of a given topic,
ranked by article volume with percentage share of total coverage.

**Parameters:**

| Parameter | Type   | Required | Default | Description |
|-----------|--------|----------|---------|-------------|
| topic     | string | No       | AI      | Market narrative to analyse sources for |

**Example request:**
```
GET http://127.0.0.1:5000/api/sources?topic=EVs
```

**Example response:**
```json
{
  "topic": "EVs",
  "sources": [
    { "source": "Reuters",   "count": 3, "share": 30.0 },
    { "source": "Bloomberg", "count": 2, "share": 20.0 },
    { "source": "BBC",       "count": 2, "share": 20.0 },
    { "source": "CNN",       "count": 1, "share": 10.0 },
    { "source": "The Guardian", "count": 1, "share": 10.0 }
  ]
}
```

**Notes:**
- Returns top 8 sources by default
- `share` is percentage of total coverage — all shares sum to ~100%
- Use `source` as chart label, `count` or `share` as chart value

---

## GET /api/summary

Generates a concise 3-4 sentence AI-written summary of what
is currently happening with a market narrative, using Claude
(Anthropic) with live headlines as context.
Summaries are cached for 1 hour to reduce API costs.

**Parameters:**

| Parameter | Type   | Required | Default | Description |
|-----------|--------|----------|---------|-------------|
| topic     | string | No       | AI      | Market narrative to summarise |

**Example request:**
```
GET http://127.0.0.1:5000/api/summary?topic=AI
```

**Example response:**
```json
{
  "topic": "AI",
  "summary": "The AI sector is experiencing significant momentum driven by Nvidia's record chip sales and continued investment into large language models. Regulatory attention is growing, with the US Senate advancing an AI oversight bill that could reshape how companies deploy models commercially. Despite this, overall market sentiment remains bullish, with valuations at record levels and major tech firms accelerating their AI infrastructure buildout.",
  "sentiment": "positive",
  "keywords": ["nvidia", "regulation", "funding", "model", "chip"],
  "cached": false
}
```

**Notes:**
- `cached: true` means the summary was served from the local database
- `cached: false` means it was freshly generated by Claude
- First call for a topic takes 2-3 seconds — subsequent calls within 1 hour are instant
- Summary is written in plain English for a general audience

---

## GET /api/topics

Returns the full narrative watchlist ranked by today's article
volume — showing which topics are getting the most coverage
right now.

**Parameters:** none

**Example request:**
```
GET http://127.0.0.1:5000/api/topics
```

**Example response:**
```json
{
  "topics": [
    { "topic": "AI",                "article_count": 10 },
    { "topic": "Bitcoin",           "article_count": 9  },
    { "topic": "Nvidia",            "article_count": 8  },
    { "topic": "Tesla",             "article_count": 6  },
    { "topic": "Inflation",         "article_count": 5  },
    { "topic": "EVs",               "article_count": 4  },
    { "topic": "Oil",               "article_count": 4  },
    { "topic": "Crypto",            "article_count": 3  },
    { "topic": "Fed",               "article_count": 3  },
    { "topic": "Quantum Computing", "article_count": 1  }
  ]
}
```

**Notes:**
- Use this for the homepage ticker and trending topics display
- Sorted by article count descending — most covered topic first
- Watchlist is configurable in `config.py` under `WATCHLIST_TOPICS`

---

## GET /api/popular

Returns the most frequently searched topics by users of the
app, pulled from the search log in the SQLite database.

**Parameters:** none

**Example request:**
```
GET http://127.0.0.1:5000/api/popular
```

**Example response:**
```json
{
  "popular_topics": [
    { "topic": "AI",      "searches": 24 },
    { "topic": "Bitcoin", "searches": 18 },
    { "topic": "Tesla",   "searches": 11 },
    { "topic": "Nvidia",  "searches": 7  },
    { "topic": "EVs",     "searches": 3  }
  ]
}
```

**Notes:**
- Returns top 5 topics by default
- Search count increments every time a topic is fetched fresh from NewsAPI
- Cached requests do not increment the count
- Use this for a "trending searches" or "popular narratives" section

---

## Error Responses

All endpoints return a consistent error format:

**400 Bad Request — empty or invalid topic:**
```json
{
  "error": "Topic cannot be empty"
}
```

**Triggers when:**
- `?topic=` is empty
- `?topic=` contains only whitespace
- Topic is sanitized to an empty string after removing special characters

**What frontend should do:**
Check `response.ok` before reading data:
```javascript
const response = await fetch("http://127.0.0.1:5000/api/news?topic=");
if (!response.ok) {
    const error = await response.json();
    console.error(error.message); // "Topic cannot be empty"
    return;
}
```

---

## Quick Reference

| Route | Key response fields | Used for |
|---|---|---|
| `/api/news?topic=` | `articles[]` | Article cards |
| `/api/sentiment?topic=` | `overall.label`, `articles[].score` | Sentiment badges |
| `/api/keywords?topic=` | `keywords[].word`, `keywords[].count` | Tag cloud |
| `/api/trend?topic=` | `trend`, `velocity`, `buckets[]` | Line chart, trend badge |
| `/api/sources?topic=` | `sources[].source`, `sources[].share` | Pie/bar chart |
| `/api/summary?topic=` | `summary` | AI summary panel |
| `/api/topics` | `topics[].topic`, `topics[].article_count` | Homepage ticker |
| `/api/popular` | `popular_topics[]` | Trending searches |
