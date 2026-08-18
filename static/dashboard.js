// Dashboard.js

const marketChart1=document.getElementById("chart-1");
const pieChart = new Chart(marketChart1, {
  type: 'pie',
  data: {
    labels:["AI","Nividia","Bitcoin","Oil","Tesla"],
    datasets:[{label:"Market Interest",data:[80,90,65,40,70]}]
  },
  options: {
    responsive: true,
    plugins: {
      legend: {
        position: 'right',
      }
    }
  },
});

const marketChart2=document.getElementById("chart-2");
const lineChart = new Chart(marketChart2, {
  type: 'line',
  data: {
    labels:trendLabels,
    datasets:[{label:"Narrative Volume",data:trendData,borderWidth:3,tension:0.4,fill:false}]
  },
  options: {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'bottom',
      }
    }
  },
});
const sidebar=document.querySelector(".sidebar");
const toggleMenu = document.querySelector(".toggle-menu");toggleMenu.addEventListener("click", function () {

    sidebar.classList.toggle("collapsed");

});

function sentimentalBadge(sentiment){
    const sentimental=document.getElementById("sentimental-badge");
    sentimental.classList.add("badge");
    if(sentiment=="positive"){
        sentimental.innerHTML=`
        <img src="../Images/Positive.png" alt="negative-badge">
        `;
    }
    else if(sentiment=="neutral"){
        sentimental.innerHTML=`
        <img src="../Images/Neutral.png" alt="negative-badge">
        `;
    }
    else{
        sentimental.innerHTML=`
        <img src="../Images/Negative.png" alt="negative-badge">
        `;
    }
}