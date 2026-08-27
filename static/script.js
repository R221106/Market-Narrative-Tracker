const API_URL = "https://market-narrative-tracker.onrender.com";
const searchInput = document.getElementById("search-input");
const searchButton = document.getElementById("search-button");
searchButton.addEventListener("click",function(){
    const topic = searchInput.value.trim();
    if(!topic) return;
    window.location.href=`search.html?topic=${encodeURIComponent(topic)}`;
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

async function getkeywords() {
    try{
        const response=await fetch( `${API_URL}/api/dashboard`); // fetching the data
        if(!response.ok) throw new Error("Failed to fetch the error!")
        const data = await response.json();
        displayKeywords(data.topics);
    }
    catch(error){
        console.error("Error fetching keywords:", error);
    } 
}

function displayKeywords(keyword){
    const track=document.getElementById("infinite-track");
    track.innerHTML="";
    const allKeyword=[...keyword,...keyword];
    //Take everything inside this array and spread it out individually.
    allKeyword.forEach(keyword=>{
        const card=document.createElement("div");
        card.classList.add("card");
        card.innerHTML=`<h2>${keyword}</h2>`
        card.addEventListener("click",function(){
            window.location.href=`search.html?topic=${encodeURIComponent(keyword)}`;
        });
        track.appendChild(card);
    });
}

getkeywords();