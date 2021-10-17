



document.getElementById("starter").addEventListener("click",check);


function check(){
    document.querySelector("img").classList.add("hider");
    document.querySelector("p").classList.add("hider");
    document.getElementById("starter").classList.add("hider");
    document.getElementsByClassName("circle").style.height = "1rem";
}