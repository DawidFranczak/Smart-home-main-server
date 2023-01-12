const calibration = (e) => {
  const mess = document.querySelector("#message");
  const event = e.type;
  const element = e.target;
  let dict = {};
  switch (event) {
    case "pointerdown":
      const calibrationButtons = document.querySelector("#calibration-buttons");
      const saveButtons = document.querySelector("#save-buttons");

      if (element.type === "button") {
        const action = element.id;
        dict = {
          action: action,
        };
      } else if (element.type === "submit") {
        if (element.innerHTML === "Zakończ") {
          dict = {
            action: "end",
          };

          calibrationButtons.classList.remove("Calibration-buttons--active");
          saveButtons.classList.add("Save-button--active");

          mess.innerHTML = "Czy chcesz powtórzyć kalibrację ?";
          break;
        } else if (element.id === "repeat") {
          dict = {
            action: "calibration",
          };

          calibrationButtons.classList.add("Calibration-buttons--active");
          saveButtons.classList.remove("Save-button--active");

          mess.innerHTML =
            "Zaczynamy kalibrację, proszę zasunąć roletę i nacisnąć przycisk 'Zapisz'";
          document.querySelector("#save").innerHTML = "Zapisz";
          break;
        } else if (element.id === "save") {
          dict = {
            action: "save",
          };

          document.querySelector("#save").innerHTML = "Zakończ";
          mess.innerHTML = "Teraz rozsuń roletę i naciśnij przycisk 'zakończ'";
        }
      }
      break;
    case "pointerup":
      if (element.type === "button") {
        dict = {
          action: "stop",
        };
      }
      break;
  }
  if (dict["action"] != undefined) sendData("POST", dict);
};

document
  .querySelector("#container")
  .addEventListener("pointerdown", calibration);
document.querySelector("#container").addEventListener("pointerup", calibration);
