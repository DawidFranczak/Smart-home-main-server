async function change_light() {
  var button = this;
  dict = { action: "change", id: this.id };
  const dataRep = await sendData("POST", dict);

  switch(dataRep["response"]){
  case 1:
    button.src = "/static/images/lamp_on.png";
    break;
  case 0:
     button.src = "/static/images/lamp_off.png";
     break;
  case -1:
    button.parentElement.nextElementSibling.innerHTML = 'Nie udało się połączyć z lampą';
    break;
  }
}

window.onload = function () {
  document.querySelectorAll(".button").forEach((b) => {
    b.addEventListener("click", change_light);
  });
};
