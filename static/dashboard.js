// Dashboard.js
const API_URL = "";
function showDashboardError(message) {
    const container = document.getElementById("news-container");

    if (container) {
        container.innerHTML = `
            <div class="error-message">
                <p>${message}</p>
            </div>
        `;
    }
}
async function loadDashboard() {
    try {
        const response = await fetch(`${API_URL}/api/dashboard`);

        if (response.status === 503) {
            showDashboardError("News service is temporarily unavailable. Try again later!");
            return;
        }

        if (!response.ok) {
            throw new Error("Failed to load dashboard data");
        }

        const data = await response.json();

        renderCharts(data.topics, data.counts);

    } catch (error) {
        console.error("Dashboard error:", error);
        showDashboardError("Unable to load dashboard data.");
    }
}

function renderCharts(topics, counts) {
    const marketChart1 = document.getElementById("chart-1");
    if (!marketChart1) {
        console.error("chart-1 canvas was not found");
        return;
    }

    new Chart(marketChart1, {
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

async function loadTopSearches() {
    try {
        const response = await fetch(`${API_URL}/api/popular`);

        if (!response.ok) {
            throw new Error("Failed to load popular topics");
        }

        const data = await response.json();

        const container = document.getElementById("top-searches");

        if (!container) return;

        container.innerHTML = "";

        data.popular_topics.forEach(item => {
            const topic = document.createElement("p");
            topic.innerHTML = `<b>${item.topic}</b> — ${item.searches} searches`;
            container.appendChild(topic);
        });

    } catch (error) {
        console.error("Top searches error:", error);
    }
}

async function loadHeadlines(topic) {
    if(!topic) return;
    try {
        const [newsResponse,sentimelResponse]= await Promise.all([
            fetch(`${API_URL}/api/news?topic=${encodeURIComponent(topic)}`),
            fetch(`${API_URL}/api/sentiment?topic=${encodeURIComponent(topic)}`
        )]);
        if (newsResponse.status === 503 || sentimelResponse.status === 503) {
            showDashboardError(
                "News service is temporarily unavailable. Try again later!"
            );
            return;
        }
        if (!newsResponse.ok) {
            throw new Error("Failed to load headlines"); }
        if (!sentimelResponse.ok) {
            throw new Error("Failed to load headlines");}
        const [newsData,sentimentalData]= await Promise.all([newsResponse.json(),sentimelResponse.json()]);
        const container = document.getElementById("news-container");
        if (!newsData.articles || newsData.articles.length === 0) {
            document.title = "Market Narrative Dashboard";
            searchInput.placeholder = "No search topic provided";
            if (container) {
                container.innerHTML = "<p> <b> No results found for this topic. </b> </p>";
            }
            return;
        }
        container.innerHTML = "";

        newsData.articles.slice(0, 5).forEach(article => {
            const card = document.createElement("div");
            const sentimentArticle=sentimentalData.articles.find(
              item=>item.url===article.url
            );
            card.innerHTML = `
                <div class="headline-title">
                    <a href="${article.url}" target="_blank" rel="noopener noreferrer">
                        <h3>${article.title}</h3>
                    </a>
                    <div class="sentiments">
                    ${getSentimentalBadge(sentimentArticle ? sentimentArticle.sentiment:"neutral")}
                    </div>
                </div>
                <p>${article.description || ""}</p> <br>
            `;

            container.appendChild(card);
        });

    } catch (error) {
        console.error("Headlines error:", error);
        showDashboardError(
            "Unable to load news. Please try again later!"
        );
    }
}

// Side bar Closing and Opening 
const sidebar=document.querySelector(".sidebar");
const toggleMenu = document.querySelector(".toggle-menu");
if(sidebar && toggleMenu){
    const sidebarState=localStorage.getItem("sidebarState");
    if(sidebarState === "collapsed") sidebar.classList.add("collapsed");
    toggleMenu.addEventListener("click", function () {
        sidebar.classList.toggle("collapsed");
        if(sidebar.classList.contains("collapsed")) {
            localStorage.setItem("sidebarState","collapsed");
        }
        else {
            localStorage.setItem("sidebarState","open");
        }
    });
}

function getSentimentalBadge(sentiment) {
    if (sentiment === "positive") {
        return `<span class="sentiment sentiment-positive">POSITIVE</span>`;
    } else if (sentiment === "neutral") {
        return `<span class="sentiment sentiment-neutral">NEUTRAL</span>`;
    } else {
        return `<span class="sentiment sentiment-negative">NEGATIVE</span>`;
    }
}

async function loadTrending(topic) {
    try {
        const response = await fetch( `${API_URL}/api/trend?topic=${encodeURIComponent(topic)}`
        );
        const trendInfo=document.getElementById("trend-info");
        if (response.status === 503) {
            if (trendInfo) {
                trendInfo.innerHTML =
                    `<p class="error-message">
                        News service is temporarily unavailable. Try again later!
                    </p>`;
            }
            return;
        }
        if (!response.ok) {
            throw new Error("Failed to load dashboard data");
        }
        const data = await response.json();
        const hours=data.buckets.map(bucket=> bucket.hour.split(" ")[1]);
        const counts=data.buckets.map(bucket=> bucket.count);
        const trendTopic=data.topic;
        const trend=data.trend;
        trendInfo.innerHTML=`Topic: ${trendTopic} | Trend:${trend}`;
        const TrendChart = document.getElementById("trend-chart");
        if (!TrendChart) {
        console.error("chart-1 canvas was not found");
        return;
    }
        new Chart(TrendChart, {
            type: "line",
            data: {
                labels: hours,
                datasets: [{label: trendTopic,data: counts , tension:0.3}]},
            options: {
                responsive: true,
                scales: {
                    x: {
                        title: {
                            display: true,
                            text: "Time"
                        }
                    },

                    y: {
                        beginAtZero: true,

                        title: {
                            display: true,
                            text: "No of Articles"
                        }
                    }
                },
                plugins: {
                    legend: {
                        position: "top"
                    }
                }
            }
        });


    } catch (error) {
        console.error("Dashboard error:", error);
        const trendInfo = document.getElementById("trend-info");
        if (trendInfo) {
            trendInfo.innerHTML = `
                <p class="error-message">
                    Unable to load trend data. Please try again later!
                </p>
            `;
        }
    }
}

async function loadSources(topic){
  try {
        const response = await fetch(`${API_URL}/api/sources?topic=${encodeURIComponent(topic)}`);
        if (response.status === 503) {
            const container = document.getElementById("top-sources-container");
            if (container) {
                container.innerHTML = `
                    <div class="error-message">
                        <p>News service is temporarily unavailable. Try again later!</p>
                    </div>
                `;
            }
            return;
        }
        if (!response.ok) throw new Error("Failed to load sources data");
        const data = await response.json();
        getSources(data.sources,topic);
        console.log(data.sources);

    } catch (error) {
        console.error("Top Sources error:", error);
        const container = document.getElementById("top-sources-container");
        if (container) {
            container.innerHTML = `
                <div class="error-message">
                    <p>Unable to load top sources. Please try again later!</p>
                </div>
            `;
        }
    }
}

function getSources(sources,topic){
  const container = document.getElementById("top-sources-container");
  container.innerHTML = "";
  if (!sources || sources.length === 0) {
        container.innerHTML = `
            <p>No Top Sources for "${topic}"</p>
        `;
        return;
    }
  sources.forEach(s => {
      const sourceCard = document.createElement("div");
      sourceCard.innerHTML = `
          <div class="source-info">
            <p><b>${s.source} </b>| ${s.count} articles </p>
            <div class="source-share">${s.share}%</div>
          </div>
          <div class="source-bar">
              <div class="source-bar-fill" style="width: ${s.share}%">
              </div>
          </div>
          <br>
      `;
      container.appendChild(sourceCard);
  });
}

async function loadSummary(topic){
    const loading = document.getElementById("summary-loading");
    const summaryContent = document.getElementById("summary-content");
    try {
        const response = await fetch(`${API_URL}/api/summary?topic=${encodeURIComponent(topic)}`);
        if (response.status === 503) {
            summaryContent.innerHTML = `
                <div class="error-message">
                    <p>News service is temporarily unavailable. Try again later!</p>
                </div>
            `;
            return;
        }
        if (!response.ok) throw new Error("Failed to load AI Summary");
        const data = await response.json();
        console.log(data.summary);
        summaryContent.innerHTML=`
            <h3>Topic: ${data.topic}</h3><br>
            <p>Sentimental Tone: ${data.sentiment}</p><br>
            <p>${data.summary}</p>
        `;
    } catch (error) {
        console.error("AI Summary error:", error);
        summaryContent.innerHTML=`<p>Unable to Generate a Summary</p>`;
    } finally{
        if(loading) loading.style.display="none";
    }
}

//For the Search DashBoard !!
// To get the topic from the URL 
const urlparams=new URLSearchParams(window.location.search);
const urlTopic =urlparams.get("topic");
const topic=urlTopic|| "AI";
const searchInput = document.getElementById("search-input");
if(topic){
    document.title=`Dashboard About ${topic}`;
    searchInput.placeholder=`Searched for ${topic}`;
    loadHeadlines(topic);
    loadSources(topic);
    loadTrending(topic);
    loadSummary(topic);
}else{
    document.title=`Market Narrative Dashboard`;
    searchInput.placeholder=`No search Topic provided`;
}
const searchButton = document.getElementById("search-button");
function performSearch(){
    const topic = searchInput.value.trim().toLowerCase().replace(/[^a-z0-9\s]/g, "").replace(/\s+/g," ");
    if(!topic) return;
    window.location.href=`dashboard.html?topic=${encodeURIComponent(topic)}`;
}

searchButton.addEventListener("click",performSearch);
searchInput.addEventListener("keydown",function(event){
    if(event.key==="Enter") performSearch();
});

window.addEventListener("load",function(){
    const loader= document.getElementById("page-loader");
    if(loader){
        loader.style.display="none";
    } 
})
loadDashboard();
loadTopSearches();