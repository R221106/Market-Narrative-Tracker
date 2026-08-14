const searchInput = document.getElementById("search-input");
const searchButton = document.getElementById("search-button");
searchButton.addEventListener("click",function(){
    const topic = searchInput.value.trim();
    if(!topic) return;
    window.location.href=`search.html?topic=${encodeURIComponent(topic)}`;
});