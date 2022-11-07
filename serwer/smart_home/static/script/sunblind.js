const sunblind = function (e){
  const sunblindValue = document.getElementById(this.placeholder);
  switch (e.type) {
    case "mousedown":
      this.oninput = function () {
        sunblindValue.innerHTML = this.value;
      };
      break;

    case "mouseup":
      let dict = { 
        action: "set", 
        value: this.value, 
        id: this.placeholder 
      };
      sendData("POST", dict)
      break;
  }
}

window.onload = function () {
  document.querySelector("#calibration").addEventListener("click", () => {
    document.querySelector(".calibration-button").classList.toggle('calibration-button-active');
    document.querySelectorAll(".cal-button").forEach((btn) => {
      btn.classList.toggle('calibration-button-active');
    });
  });

  document.querySelectorAll(".slider").forEach((slider) => {
    slider.addEventListener("mousedown",sunblind);
    slider.addEventListener("mouseup", sunblind);
  });
};
