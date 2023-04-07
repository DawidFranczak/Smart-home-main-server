function translation(){
  const LANG = window.navigator.language;
  if (LANG === "pl-PL"){
      let TRANSLATE = {
         "FSTEP":'Zaczynamy kalibrację, proszę rozsunąć roletę i nacisnąć przycisk "Zapisz"',
         "SSTEP":'Teraz rozsuń roletę i naciśnij przycisk "Zapisz"',
         "REPLAY":"Czy chcesz powtórzyć kalibrację ?",
      }
  return TRANSLATE
  }else{
      let TRANSLATE = {
        "FSTEP":'During the calibration process, please open the sunblind and press "save" button',
        "SSTEP":'Now close the sunblind and press "Save".',
        "REPLAY":'Do you want to repeat the calibration process?',

      }
  return TRANSLATE
  }
}


const calibration = (e) => {
  const mess = document.querySelector("#message");
  const event = e.type;
  const element = e.target;
  let action;
  const TR = translation()

  if (event === "pointerdown") {
    const calibrationButtons = document.querySelector("#calibration-buttons");
    const saveButtons = document.querySelector("#save-buttons");
    if (element.type === "button") {
      action = element.id;
    } else if (element.id === "save") {
      action = "save";
      element.id = "end";
      mess.innerHTML = TR["SSTEP"];
    } else if (element.id === "end") {
      action = "end";
      element.id = "save";
      mess.innerHTML = TR["REPLAY"];
      calibrationButtons.classList.remove("Calibration-buttons--active");
      saveButtons.classList.add("Save-button--active");
    } else if (element.id === "repeat") {
      action = "calibration";
      mess.innerHTML = TR["FSTEP"];
      calibrationButtons.classList.add("Calibration-buttons--active");
      saveButtons.classList.remove("Save-button--active");
    }
  } else if (event === "pointerup") {
    if (element.type === "button") action = "stop";
  }
  dict = { action: action };
  if (dict["action"] != undefined) sendData("PUT", dict,"/update/");
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
