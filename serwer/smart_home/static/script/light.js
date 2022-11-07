async function changeLight() {
  const lamp = this;

  dict = { 
    action: "change", 
    id: lamp.id 
  };
  const dataRep = await sendData("POST", dict);

  switch(dataRep["response"]){
  case 1:
    lamp.src = "/static/images/lamp_on.png";
    break;
  case 0:
     lamp.src = "/static/images/lamp_off.png";
     break;
  case -1:
    lamp.parentElement.nextElementSibling.innerHTML = 'Nie udało się połączyć z lampą';
    break;
  }
}

window.onload = function () {
  document.querySelectorAll(".button").forEach((b) => {
    b.addEventListener("click", changeLight);
  });
};
