const calibration = (e) => {
  const mess = document.querySelector("#message");
  const event = e.type;
  const element = e.target
  let dict = {}
  switch (event) {
  case "mousedown":
    if(element.type === "image"){
      const action = element.id;
      dict = { 
        action: action 
      };
    }
    else if(element.type === "submit") {
      if (element.innerHTML === "Zakończ") {
        dict = {
           action: "end" 
        };
        document.querySelector("#calibration-buttons").classList.remove('Calibration-buttons--active')
        document.querySelector("#save-buttons").classList.add('Save-button--active')
        mess.innerHTML = "Czy chcesz powtórzyć kalibrację ?";
        break;
      } else if (element.id === "repeat") {
        dict = { 
          action: "calibration" 
        };
        document.querySelector("#calibration-buttons").classList.add('Calibration-buttons--active')
        document.querySelector("#save-buttons").classList.remove('Save-button--active')
        document.querySelector("#save").innerHTML = "Zapisz";
        mess.innerHTML =
          "Zaczynamy kalibrację, proszę zasunąć roletę i nacisnąć przycisk 'Zapisz'";
        break;
      }
      dict = { 
        action: "save" 
      };
      document.querySelector("#save").innerHTML = "Zakończ";
      mess.innerHTML = "Teraz rozsuń roletę i naciśnij przycisk 'zakończ'";
    }
    break;
  }
  if(dict['action'] != undefined) sendData("POST", dict);
}
window.onload = function () {
  document.querySelector("#container").addEventListener("mousedown", calibration);
  document.querySelector("#container").addEventListener("mouseup", calibration);
};
