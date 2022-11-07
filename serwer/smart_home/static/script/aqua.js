const selectAqua = async function() {
  id = this.id;

  settings = await fetch(`/api/akwarium/${id}`);
  settings = await settings.json();

  console.log(settings)
  
  const containerAqua = document.querySelector("#containers-aqua");
  containerAqua.classList.toggle("active-aqua");
  containerAqua.setAttribute("placeholder", id);

  document.querySelector("#fluolamp-start").value = settings["fluo_start"];
  document.querySelector("#fluolamp-stop").value = settings["fluo_stop"];
  document.querySelector("#led-start").value = settings["led_start"];
  document.querySelector("#led-stop").value = settings["led_stop"];

  document.querySelector('#mess').innerHTML = `Wybrano ${this.value}`

  const mode = document.querySelector("#mode");
  const modeButton = document.querySelector("#mode-buttons");
  const settingsAqua = document.querySelector("#settings-aqua");

  if (settings["mode"]) {
    mode.value = "Automat";
    modeButton.style.display = "";
    settingsAqua.style.display = "none";
  } else {
    mode.value = "Ręczny";
    modeButton.style.display = "none";
    settingsAqua.style.display = "";
  }

  const modeFluoLampButton = document.querySelector("#mode-button-fluolamp");
  const modeLedButton = document.querySelector("#mode-button-led");

  modeFluoLampButton.value = settings["fluo_mode"] ? "Wyłącz" : "Włącz";
  modeLedButton.value = settings["led_mode"] ? "Wyłącz" : "Włącz";
}

const aqua = async function() {
  let dict = {};
  const id = document.querySelector("#containers-aqua").getAttribute("placeholder");
  const action = this.id;

  switch (action){
  case 'color':
    const aqua = document.querySelector("#color");
    const color = aqua.value.substring(4, aqua.value.length - 1).split(",");

    const [r,g,b] = color
        dict = {
          action: "changeRGB",
          r: r,
          g: g,
          b: b,
          id: id
        };
    break;
  case 'led-button':
    const ledStart = document.querySelector("#led-start");
    const ledStop = document.querySelector("#led-stop");

    if (ledStart.value === "" || ledStop.value === "") {
      document.querySelector("#led-mess").innerHTML = "Brak jednej godziny";
    } else {
        dict = {
        action: "changeLedTime",
        ledStart: ledStart.value,
        ledStop: ledStop.value,
        id: id
      };
    }
    break;
  case 'fluolamp-button':
    const fluoLampStart = document.querySelector("#fluolamp-start");
    const fluoLampStop = document.querySelector("#fluolamp-stop");

    if (fluoLampStart.value === "" || fluoLampStop.value === "") {
      document.querySelector("fluolamp-mess").innerHTML = "Brak jednej godziny";
    } 
    else {
      dict = {
        action: "changeFluoLampTime",
        fluoLampStart: fluoLampStart.value,
        fluoLampStop: fluoLampStop.value,
        id: id
      };
    }
    break;
  case 'mode':
    let mode = false;
    const modeButton = this;

    if (modeButton.value === "Ręczny") {
      mode = true;
      modeButton.value = "Automat";
      document.querySelector("#mode-buttons").style.display = "";
      document.querySelector("#settings-aqua").style.display = "none";
    } 
    else {
      modeButton.value = "Ręczny";
      document.querySelector("#mode-buttons").style.display = "none";
      document.querySelector("#settings-aqua").style.display = "";
    }

    dict = {
      action: "changeMode",
      mode: mode,
      id: id
    };

    data = await sendData("POST", dict);
    console.log(data)

    const modeFluolampButton = document.querySelector("#mode-button-fluolamp");
    const modeLedButton = document.querySelector("#mode-button-led");

    modeFluolampButton.value = data["fluo"] ? "Wyłącz" : "Włącz";
    modeLedButton.value = data["led"] ? "Wyłącz" : "Włącz";

    break;
  case 'mode-button-fluolamp':
    let valueFluolamp = false;
    const fluolampMode = this;

    if (fluolampMode.value === "Włącz") {
      fluolampMode.value = "Wyłącz";
      valueFluolamp = true;
    } else {
      fluolampMode.value = "Włącz";
    }

    dict = {
      action: "changeFluoLampState",
      value: valueFluolamp,
      id: id
    };
    break;
  case 'mode-button-led':
    let valueLed = false;
    const ledMode = this;

    if (ledMode.value === "Włącz") {
      ledMode.value = "Wyłącz";
      valueLed = true;
    } 
    else {
      ledMode.value = "Włącz";
    }
    dict = {
      action: "changeLedState",
      value: valueLed,
      id: id
    };
    break;
  }

  const rep = await sendData("POST", dict);

  if (rep['success']){
    switch (rep['success']){
    case 1:
      console.log(1);
      break;
    case 2:
      console.log(2)
      break;
    }
  }
  else{
    switch (rep['error']){
      case -1:
        console.log(-1);
        break;
      case -2:
        console.log(-2)
        break;
      }
  }

}

window.onload = function () {
  document.querySelectorAll(".button").forEach((b) => {
    b.addEventListener("click", selectAqua);
  });
  
  document.querySelector("#color").addEventListener("input", aqua);
  document.querySelector("#led-button").addEventListener("click", aqua);
  document.querySelector("#fluolamp-button").addEventListener("click", aqua);
  document.querySelector("#mode").addEventListener("click", aqua);
  document.querySelector("#mode-button-led").addEventListener("click", aqua);
  document.querySelector("#mode-button-fluolamp").addEventListener("click", aqua);
};
