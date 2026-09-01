const API_URL = "";
async function getData(topic) {
    try{
        const response=await fetch( `${API_URL}/api/news?topic=${encodeURIComponent(topic)}`); // fetching the data
        if (response.status === 503) {
            showError("News service is temporarily unavailable. Try again later!");
            return;
        }
        if(!response.ok) throw new Error("Failed to fetch the error!")
        const data = await response.json();
        fetchNews(data.articles);
    }
    catch(error){
        console.error("Error fetching news:", error);
        const searchResult=document.getElementById("search-results");
        searchResult.innerHTML=`<p>Unable to load news. Please Try Again!</p>`;
    } 
}
function showError(message){
    const container = document.getElementById("search-results")
    container.innerHTML=`
        <div class="error-message">
            <p>${message}</p>
        </div>
    `;
}

function fetchNews(article){
    const searchResult = document.getElementById("search-results")
    searchResult.innerHTML="";
    // for each article news created a seperate div element is created dynamically !!
    if(!article || article.length===0){
        searchResult.innerHTML=`
        <p>No search Result Found !</p>
        `;
        return;
    }
    
    document.getElementById("result-count").textContent=`${article.length} Articles Found`
    
    article.forEach(element => {
        const newsCard=document.createElement("div");
        newsCard.classList.add("newsCard"); //<div class="newsCard"></div>
        newsCard.innerHTML=`
                <a href="${element.url}" target="_blank" rel="noopener noreferrer">
                    <h3>${element.title}</h3>
                </a>
                <p>${element.description || "No description Available.."}</p> <br>
        `;
        searchResult.append(newsCard)
    });
}

async function loadSummary(topic){
    const loading = document.getElementById("summary-loading");
    const summaryContent = document.getElementById("summary-content");
    try {
        const response = await fetch(`${API_URL}/api/summary?topic=${encodeURIComponent(topic)}`);
        if (!response.ok) throw new Error("Failed to load AI Summary");
        const data = await response.json();
        console.log(data.summary);
        summaryContent.innerHTML=`
            <h3>${data.topic}</h3><br>
            <p>${data.sentiment}</p><br>
            <p>${data.summary}</p>
        `;
        if (loading) {
            loading.style.display = "none";
        }
    } catch (error) {
        console.error("AI Summary error:", error);
        if (loading) {
            loading.style.display = "none";
        }
        if (summaryContent) {
            summaryContent.innerHTML = `<p>Unable to Generate a Summary</p>`;
        }
    }
}

// To get the topic from the URL 
const urlparams=new URLSearchParams(window.location.search);
const topic =urlparams.get("topic");
const searchTopic=document.getElementById("search-topic");
const searchInput = document.getElementById("search-input");
if(topic){
    document.title=`Search for ${topic}`;
    searchTopic.textContent=`You searched for ${topic}`;
    searchInput.placeholder=`Searched for ${topic}`;
    getData(topic);
    loadSummary(topic);
}else{
    searchTopic.textContent=`No search Topic provided`;
}
const searchButton = document.getElementById("search-button");
function performSearch(){
    const topic = searchInput.value.trim().toLowerCase().replace(/[^a-z0-9\s]/g, "").replace(/\s+/g," ");
    if(!topic) return;
    window.location.href=`search.html?topic=${encodeURIComponent(topic)}`;
}
searchButton.addEventListener("click",performSearch);
searchInput.addEventListener("keydown",function(event){
    if(event.key==="Enter") performSearch();
});

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

window.addEventListener("load",function(){
    const loader= document.getElementById("page-loader");
    if(loader){
        loader.style.display="none";
    } 
})