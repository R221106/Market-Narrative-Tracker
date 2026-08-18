// Dashboard.js

async function loadDashboard() {
    try {
        const response = await fetch("http://127.0.0.1:5000/api/dashboard");

        if (!response.ok) {
            throw new Error("Failed to load dashboard data");
        }

        const data = await response.json();

        renderCharts(data.topics, data.counts);
        loadHeadlines();

    } catch (error) {
        console.error("Dashboard error:", error);
    }
}

function renderCharts(topics, counts) {
    const marketChart1 = document.getElementById("chart-1");

    new Chart(marketChart1, {
        type: "pie",
        data: {
            labels: topics,
            datasets: [
                {
                    label: "Market Interest",
                    data: counts
                }
            ]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: "right"
                }
            }
        }
    });

    const marketChart2 = document.getElementById("chart-2");

    new Chart(marketChart2, {
        type: "line",
        data: {
            labels: topics,
            datasets: [
                {
                    label: "Market Interest",
                    data: counts
                }
            ]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: "bottom"
                }
            }
        }
    });
}

async function loadHeadlines() {
    try {
        const newsResponse = await fetch(
            "http://127.0.0.1:5000/api/news?topic=AI"
        );

        if (!newsResponse.ok) {
            throw new Error("Failed to load headlines");
        }

        const newsData = await newsResponse.json();

        const sentimelResponse = await fetch(
            "http://127.0.0.1:5000/api/sentiment?topic=AI"
        );

        if (!sentimelResponse.ok) {
            throw new Error("Failed to load headlines");
        }

        const sentimentalData = await sentimelResponse.json();


        const container = document.getElementById("news-container");

        container.innerHTML = "";

        newsData.articles.slice(0, 5).forEach(article => {
            const card = document.createElement("div");
            const sentimentArticle=sentimentalData.articles.find(
              item=>item.url===article.url
            );
            card.innerHTML = `
                <div class="headline-title">
                    <h3>${article.title}</h3>
                    <div class="sentiments">
                    ${getSentimentalBadge(sentimentArticle ? sentimentArticle.sentiment:"neutral")}
                    </div>
                </div>
                <p>${article.description || ""}</p>
                <a href="${article.url}" target="_blank">Read more</a>
                <hr>
            `;

            container.appendChild(card);
        });

    } catch (error) {
        console.error("Headlines error:", error);
    }
}

const sidebar = document.querySelector(".sidebar");
const toggleMenu = document.querySelector(".toggle-menu");

if (toggleMenu) {
    toggleMenu.addEventListener("click", function () {
        sidebar.classList.toggle("collapsed");
    });
}

function getSentimentalBadge(sentiment) {
    if (sentiment === "positive") {
        return `
            <img
                src="../Images/Positive.png"
                alt="positive-badge"
            >
        `;
    } else if (sentiment === "neutral") {
        return `
            <img
                src="../Images/Neutral.png"
                alt="neutral-badge"
            >
        `;
    } else {
        return `
            <img
                src="../Images/Negative.png"
                alt="negative-badge"
            >
        `;
    }
}

loadDashboard();