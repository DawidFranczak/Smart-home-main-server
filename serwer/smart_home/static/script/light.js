async function change_light() {
  var button = this;
  dict = { action: "change", id: this.id };
  dataRep = await sendData("POST", dict);

  if (dataRep["response"] == 1) button.src = "/static/images/lamp_on.png";
  else button.src = "/static/images/lamp_off.png";
}

window.onload = function () {
  document.querySelectorAll(".button").forEach((b) => {
    b.addEventListener("click", change_light);
  });
};
