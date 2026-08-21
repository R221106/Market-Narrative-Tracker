// Dashboard.js

async function loadDashboard() {
    try {
        const response = await fetch("http://127.0.0.1:5000/api/dashboard");

        if (!response.ok) {
            throw new Error("Failed to load dashboard data");
        }

        const data = await response.json();

        renderCharts(data.topics, data.counts);

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

async function loadHeadlines(topic) {
    if(!topic) return;
    try {
        const newsResponse = await fetch(
            `http://127.0.0.1:5000/api/news?topic=${encodeURIComponent(topic)}`
        );

        if (!newsResponse.ok) {
            throw new Error("Failed to load headlines");
        }

        const newsData = await newsResponse.json();

        const sentimelResponse = await fetch(
            `http://127.0.0.1:5000/api/sentiment?topic=${encodeURIComponent(topic)}`
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
                    <a href="${article.url}" target="_blank">
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
    }
}

const sidebar=document.querySelector(".sidebar");
const toggleMenu = document.querySelector(".toggle-menu");
if(sidebar && toggleMenu){
    const sidebarState=localStorage.getItem("sidebarState");
    if(sidebarState === "collapsed") sidebar.classList.add("collapsed");
}
toggleMenu.addEventListener("click", function () {
    sidebar.classList.toggle("collapsed");
    if(sidebar.classList.contains("collapsed")) localStorage.setItem("sidebarState","collapsed");
    else localStorage.setItem("sidebarState","open");
});

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

async function loadTrending(topic) {
    try {
        const response = await fetch( `http://127.0.0.1:5000/api/trend?topic=${encodeURIComponent(topic)}`
        );
        if (!response.ok) {
            throw new Error("Failed to load dashboard data");
        }
        const data = await response.json();
        const hours=data.buckets.map(bucket=> bucket.hour.split(" ")[1]);
        const counts=data.buckets.map(bucket=> bucket.count);
        const trendTopic=data.topic;
        const trend=data.trend;
        const trendInfo=document.getElementById("trend-info");
        trendInfo.innerHTML=`Topic: ${trendTopic} | Trend:${trend}`;
        const TrendChart = document.getElementById("trend-chart");

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
    }
}

async function loadSources(topic){
  try {
        const response = await fetch(`http://127.0.0.1:5000/api/sources?topic=${encodeURIComponent(topic)}`);
        if (!response.ok) throw new Error("Failed to load sources data");
        const data = await response.json();
        getSources(data.sources);
        console.log(data.sources);

    } catch (error) {
        console.error("Top Sources error:", error);
    }
}

function getSources(sources){
  const container = document.getElementById("top-sources-container");
  container.innerHTML = "";
  sources.forEach(s => {
      const sourceCard = document.createElement("div");
      sourceCard.innerHTML = `
          <div class="source-info">
            <p><b>${s.source} </b>| ${s.count} articles <p>
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
loadDashboard();