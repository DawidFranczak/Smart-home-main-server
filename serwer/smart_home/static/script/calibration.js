const calibration = function(e) {
  const mess = document.querySelector("#message");
  const event = e.type;
  switch (event) {
  case "mousedown":

    const action = this.id;
    dict = { 
      action: action 
    };
    break;
  case "mouseup":

    dict = { 
      action: "stop" 
    };

    break;
  case "click":
    const state = this;
    if (state.value === "Zakończ") {

      dict = {
         action: "end" 
      };

      document.querySelector("#clb-btn").classList.remove('active')
      document.querySelector("#conf-button").classList.add('active')
      mess.innerHTML = "Czy chcesz powtórzyć kalibrację ?";

      break;
    } else if (state.id === "rep") {

      dict = { 
        action: "calibration" 
      };

      document.querySelector("#clb-btn").classList.add('active')
      document.querySelector("#conf-button").classList.remove('active')
      document.querySelector("#save").value = "Zapisz";
      mess.innerHTML =
        "Zaczynamy kalibrację, proszę zasunąć roletę i nacisnąć przycisk 'zapisz'";
        
      break;
    }

    dict = { 
      action: "save" 
    };
    
    document.querySelector("#save").value = "Zakończ";
    mess.innerHTML = "Teraz rozsuń roletę i naciśnij przycisk 'zakończ'";
    break;
  }
  sendData("POST", dict);
}

window.onload = function () {
  document.querySelector("#up").addEventListener("mousedown", calibration);
  document.querySelector("#up").addEventListener("mouseup", calibration);
  document.querySelector("#down").addEventListener("mousedown", calibration);
  document.querySelector("#down").addEventListener("mouseup", calibration);
  document.querySelector("#save").addEventListener("click", calibration);
  document.querySelector("#rep").addEventListener("click", calibration);
};
