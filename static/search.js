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
                <h3>${element.title}</h3>
                <p>${element.description || "No desciption Available."}</p> <br>
        `;
        searchResult.append(newsCard)
    });
}

// To get the topic from the URL 
const urlparams=new URLSearchParams(window.location.search);
const topic =urlparams.get("topic");
const searchTopic=document.getElementById("search-topic");
if(topic){
    searchTopic.textContent=`You searched for ${topic} `;
    getData(topic);
}else{
    searchTopic.textContent=`No search Topic provided`;
}
const searchInput = document.getElementById("search-input");
const searchButton = document.getElementById("search-button");
searchButton.addEventListener("click",function(){
    const topic = searchInput.value.trim();
    if(!topic) return;
    window.location.href=`search.html?topic=${encodeURIComponent(topic)}`;
});