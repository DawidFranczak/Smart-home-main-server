const sunblind = async (e) => {
  const slider = e.target;
  const sunblindValue = document.getElementById(slider.placeholder);
  if (e.target.type === "range") {
    switch (e.type) {
      case "pointermove":
        sunblindValue.innerHTML = slider.value;
        sunblindValue.classList.remove(
          "Sunblind-containers__div__slider-value--error"
        );
        break;
      case "pointerup":
        let dict = {
          action: "set",
          value: slider.value,
          id: slider.placeholder,
        };
        let rep = await sendData("POST", dict);
        if (rep['status']=== 504) {
          rep = await rep.json()

          sunblindValue.innerHTML = rep["message"];
          sunblindValue.classList.add(
            "Sunblind-containers__div__slider-value--error"
          );
        }
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

document.querySelector("#container").addEventListener("pointermove", sunblind);
document.querySelector("#container").addEventListener("pointerup", sunblind);
document.querySelector("#container").addEventListener("pointerdown", sunblind);
