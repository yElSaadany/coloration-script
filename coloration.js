const sentences = document.getElementsByClassName("sen");

function fun(element) {
  return function(e) {
    let infoBlock = document.createElement("div");
    infoBlock.setAttribute("id", "infoBlock");
    infoBlock.setAttribute("class", "infoBlock");
    infoBlock.innerHTML = "<h1>" + Math.round(element.getAttribute("id") * 100) / 100 + "</h1>";
    infoBlock.style.top = e.clientY + "px";
    infoBlock.style.left = e.clientX + "px";
    infoBlock.style.backgroundColor = "grey";
    document.body.appendChild(infoBlock);
  };
}

function removeInfo(e) {
  const infoBlock = document.getElementById("infoBlock");
  document.body.removeChild(infoBlock);
}

console.log(sentences);
for (let sentence of sentences) {
  sentence.addEventListener("mouseleave", removeInfo, false);
  sentence.addEventListener("mouseenter", fun(sentence), false);
}
