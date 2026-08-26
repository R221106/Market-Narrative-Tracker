# Frontend Documentation — Market Narrative Tracker

## 1. Overview

The Market Narrative Tracker frontend provides an interactive interface for exploring financial and corporate market information.

Users can:

* Search for market topics.
* View recent news.
* View sentiment analysis.
* View market trends.
* View important news sources.
* Generate AI-based market summaries.
* Navigate between Home, Trending, Dashboard, and Search pages.

The frontend is built using **HTML, CSS, JavaScript, and Chart.js**.

---

## 2. Frontend Structure

The frontend is organised into separate HTML, CSS, and JavaScript files.

```text
frontend/
│
├── index.html
├── dashboard.html
├── search.html
├── Trending.html
│
├── style.css
├── style-dashboard.css
├── style-search.css
├── style-trending.css
│
├── script.js
├── dashboard.js
├── search.js
└── trending.js
```

Images and background video are stored separately in the project assets folders.

---

## 3. UI Modules

### Navigation Sidebar

The sidebar provides navigation between the main sections of the application.

It contains:

* Home
* Trending
* Dashboard
* Navigation toggle

The sidebar can be collapsed to provide more screen space.

The collapsed state is stored using browser `localStorage`, allowing the user's preference to remain after navigation.

---

### Search Module

The search module allows users to enter a market topic such as:

```text
AI
Oil
Tesla
Nvidia
Bitcoin
```

The entered topic is passed to the appropriate dashboard or search page.

JavaScript handles:

* Reading the search input.
* Validating the input.
* Encoding the topic.
* Navigating to the selected topic.

---

### News Module

The news module displays recent articles related to the selected topic.

Each news item can contain:

* Article title.
* Description.
* Source.
* Link to the original article.
* Sentiment indicator.

News data is retrieved from the Flask backend through the `/api/news` endpoint.

---

### Sentiment Module

The sentiment module displays the overall sentiment of the selected topic and individual article sentiment.

The main sentiment categories are:

```text
Positive
Neutral
Negative
```

These are displayed using visual sentiment badges.

---

### Trend Module

The trend module displays changes in article activity over time.

Chart.js is used to create the trend visualisation.

The data is retrieved from:

```text
/api/trend
```

---

### Sources Module

The sources module shows the major news sources contributing articles to the selected topic.

It displays:

* Source name.
* Number of articles.
* Percentage/share.

---

### AI Summary Module

The AI Summary module provides a short narrative describing the current market topic.

It displays:

* Topic.
* Overall sentiment.
* AI-generated market narrative.

The summary is retrieved through:

```text
/api/summary?topic=<topic>
```

A loading animation is displayed while the summary is being generated.

If the AI service is unavailable, an error message is shown instead.

---

## 4. API Communication

The frontend communicates with the Flask backend using JavaScript's `fetch()` API.

Main endpoints include:

```text
/api/news
/api/sentiment
/api/keywords
/api/trend
/api/sources
/api/dashboard
/api/summary
```

Topic-based requests use the `topic` query parameter.

Example:

```text
/api/news?topic=oil
```

The JavaScript receives the JSON response and dynamically updates the relevant HTML elements.

---

# 5. CSS Architecture

The stylesheets are organised into standard sections to make them easier to maintain.

The recommended structure is:

```css
/* =========================
   1. RESET & GLOBAL STYLES
   ========================= */

/* =========================
   2. PAGE LAYOUT
   ========================= */

/* =========================
   3. NAVIGATION / SIDEBAR
   ========================= */

/* =========================
   4. BACKGROUND & OVERLAY
   ========================= */

/* =========================
   5. SEARCH COMPONENT
   ========================= */

/* =========================
   6. NEWS / CONTENT CARDS
   ========================= */

/* =========================
   7. DASHBOARD COMPONENTS
   ========================= */

/* =========================
   8. AI SUMMARY
   ========================= */

/* =========================
   9. LOADING STATES
   ========================= */

/* =========================
   10. RESPONSIVE DESIGN
   ========================= */

/* =========================
   11. ANIMATIONS
   ========================= */
```

This organisation makes it easier to locate and modify styles without affecting unrelated components.

---

# 6. Responsive Design

The frontend has been designed to work across desktop, tablet, and mobile screen sizes.

Responsive CSS uses media queries to adjust:

* Sidebar width.
* Search bar size.
* Content layout.
* News cards.
* Charts.
* AI summary panels.

Example:

```css
@media (max-width: 768px) {
    .search-layout {
        grid-template-columns: 1fr;
    }
}
```

This allows multi-column content to become a single-column layout on smaller screens.

---

# 7. Loading and Error Handling

Loading animations are used when information takes time to retrieve.

For example, the AI Summary displays a loading indicator while waiting for the backend response.

JavaScript also handles failed API requests using `try...catch`.

This prevents a failed API request from breaking the entire page.

---

# 8. UI Usage Guide

### Searching for a Topic

1. Open the Dashboard or Search page.
2. Enter a market topic into the search bar.
3. Click the search button or press **Enter**.
4. The selected topic is loaded.
5. News, sentiment, trends, sources, and AI information are displayed.

### Using the Sidebar

1. Click the navigation menu icon.
2. The sidebar expands or collapses.
3. Select the required section.
4. The selected page opens.

### Viewing News

Click an article headline to open the original news source in a new browser tab.

### Viewing AI Summary

The AI Summary panel automatically loads information for the selected topic.

---

# 9. Browser Compatibility Testing

The frontend should be tested on:

* Google Chrome
* Microsoft Edge
* Mozilla Firefox
* Mobile Chrome

Testing should cover:

* Page layout.
* Search functionality.
* Sidebar.
* Charts.
* News cards.
* AI Summary.
* Loading animations.
* Mobile responsiveness.

Any browser-specific UI issues should be recorded and resolved through the relevant HTML, CSS, or JavaScript component.

---

# 10. Maintenance Guidelines

To keep the frontend maintainable:

* Keep HTML, CSS, and JavaScript separated.
* Organise CSS using clear section headings.
* Keep responsive styles together.
* Use meaningful class and ID names.
* Avoid unnecessary inline styles.
* Reuse existing UI components where possible.
* Handle API failures gracefully.
* Test changes on both desktop and mobile screens.

The CSS architecture and frontend documentation provide a consistent structure for future development and make the application easier to maintain and extend.
