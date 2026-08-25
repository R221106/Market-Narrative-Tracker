console.log("SEARCH.JS LOADED");
async function getData(topic) {
    try{
        const response=await fetch( `http://127.0.0.1:5000/api/news?topic=${encodeURIComponent(topic)}`); // fetching the data
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
                <a href="${element.url}" target="_blank">
                    <h3>${element.title}</h3>
                </a>
                <p>${element.description || "No desciption Available."}</p> <br>
        `;
        searchResult.append(newsCard)
    });
}

async function loadSummary(topic){
    const loading = document.getElementById("summary-loading");
    const summaryContent = document.getElementById("summary-content");
    try {
        const response = await fetch(`http://127.0.0.1:5000/api/summary?topic=${encodeURIComponent(topic)}`);
        if (!response.ok) throw new Error("Failed to load AI Summary");
        const data = await response.json();
        console.log(data.summary);
        summaryContent.innerHTML=`
            <h3>${data.topic}</h3><br>
            <p>${data.sentiment}</p><br>
            <p>${data.summary}</p>
        `;
        loading.style.display = "none";
    } catch (error) {
        console.error("AI Summary error:", error);
        loading.style.display = "none";
        summaryContent.innerHTML=`<p>Unable to Generate a Summary</p>`;
    }
}

// To get the topic from the URL 
const urlparams=new URLSearchParams(window.location.search);
const topic =urlparams.get("topic");
const searchTopic=document.getElementById("search-topic");
const searchInput = document.getElementById("search-input");
document.title=`Search for ${topic}`;
if(topic){
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