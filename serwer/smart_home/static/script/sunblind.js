const sunblind = (e) => {
  const slider = e.target;
  const sunblindValue = document.getElementById(slider.placeholder);
  if (e.target.type === "range") {
    switch (e.type) {
      case "pointermove":
        sunblindValue.innerHTML = slider.value;
        break;
      case "pointerup":
        let dict = {
          action: "set",
          value: slider.value,
          id: slider.placeholder,
        };
        sendData("POST", dict);
        break;
    }
  } else if (e.target.type === "submit" && e.type === "pointerdown") {
    document.querySelectorAll("#button-calibration").forEach((button) => {
      button.classList.toggle(
        "Sunblind-containers__calibration-button--avtive"
      );
    });
  }
};

window.onload = function () {
  document
    .querySelector("#container")
    .addEventListener("pointermove", sunblind);
  document.querySelector("#container").addEventListener("pointerup", sunblind);
  document
    .querySelector("#container")
    .addEventListener("pointerdown", sunblind);
};
