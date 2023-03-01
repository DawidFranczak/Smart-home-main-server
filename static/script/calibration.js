const calibration = (e) => {
  const mess = document.querySelector("#message");
  const event = e.type;
  const element = e.target;
  let action;

  if (event === "pointerdown") {
    const calibrationButtons = document.querySelector("#calibration-buttons");
    const saveButtons = document.querySelector("#save-buttons");
    if (element.type === "button") {
      action = element.id;
    } else if (element.id === "save") {
      action = "save";
      element.id = "end";
      mess.innerHTML = 'Teraz rozsuń roletę i naciśnij przycisk "Zapisz"';
    } else if (element.id === "end") {
      action = "end";
      element.id = "save";
      mess.innerHTML = "Czy chcesz powtórzyć kalibrację ?";
      calibrationButtons.classList.remove("Calibration-buttons--active");
      saveButtons.classList.add("Save-button--active");
    } else if (element.id === "repeat") {
      action = "calibration";
      mess.innerHTML =
        'Zaczynamy kalibrację, proszę zasunąć roletę i nacisnąć przycisk "Zapisz"';
      calibrationButtons.classList.add("Calibration-buttons--active");
      saveButtons.classList.remove("Save-button--active");
    }
  } else if (event === "pointerup") {
    if (element.type === "button") action = "stop";
  }
  dict = { action: action };
  if (dict["action"] != undefined) sendData("POST", dict);
};

(() => {
  const selectors = ["up", "down"];
  const events = ["pointerdown", "pointerup"];

  for (let event of events) {
    document.querySelector("#container").addEventListener(event, calibration);
  }

  for (let selector of selectors) {
    document
      .querySelector(`#${selector}`)
      .addEventListener("contextmenu", function (event) {
        event.preventDefault();
      });
  }
})();
