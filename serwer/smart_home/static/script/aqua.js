const selectAqua = async (e) => {
  if (e.target.type === 'submit'){
    id = e.target.id;

    settings = await fetch(`/api/akwarium/${id}`);
    settings = await settings.json();

    const containerAqua = document.querySelector("#containers-aqua");
    containerAqua.classList.add("Containers-aqua--active");
    containerAqua.setAttribute("placeholder", id);

    document.querySelector("#fluolamp-start").value = settings["fluo_start"];
    document.querySelector("#fluolamp-stop").value = settings["fluo_stop"];
    document.querySelector("#led-start").value = settings["led_start"];
    document.querySelector("#led-stop").value = settings["led_stop"];

    document.querySelector('#select').innerHTML = `Wybrano ${e.target.innerHTML}`

    const mode = document.querySelector("#mode");
    const modeButton = document.querySelector("#mode-buttons");
    const settingsAqua = document.querySelector("#settings-aqua");

    if (settings["mode"]) {
      mode.innerHTML = "Automat";
      modeButton.classList.add('Containers-aqua__mode-buttons--active');
      settingsAqua.classList.remove('Containers-aqua__settings-aqua--active');
    } else {
      mode.innerHTML = "Ręczny";
      modeButton.classList.remove('Containers-aqua__mode-buttons--active');
      settingsAqua.classList.add('Containers-aqua__settings-aqua--active');
    }

    const modeFluoLampButton = document.querySelector("#mode-button-fluolamp");
    const modeLedButton = document.querySelector("#mode-button-led");

    modeFluoLampButton.innerHTML = settings["fluo_mode"] ? "Wyłącz" : "Włącz";
    modeLedButton.innerHTML = settings["led_mode"] ? "Wyłącz" : "Włącz";

    document.querySelector('#containers-aqua').addEventListener('click',aqua);

  }
}

const aqua = async (e) => {
  if(e.target.type === 'submit' || e.target.id === 'color'){
    let dict = {};
    const id = document.querySelector("#containers-aqua").getAttribute("placeholder");
    const action = e.target.id;

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
      const modeButton = e.target;
        console.log(e.target)
      if (modeButton.innerHTML === "Ręczny") {
        mode = true;
        modeButton.innerHTML = "Automat";
        document.querySelector("#mode-buttons").classList.add('Containers-aqua__mode-buttons--active');
        document.querySelector("#settings-aqua").classList.remove('Containers-aqua__settings-aqua--active');
      } 
      else {
        modeButton.innerHTML = "Ręczny";
        document.querySelector("#mode-buttons").classList.remove('Containers-aqua__mode-buttons--active');
        document.querySelector("#settings-aqua").classList.add('Containers-aqua__settings-aqua--active');
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
}

window.onload = function () {
  document.querySelector('#select-aqua').addEventListener('click',selectAqua);
  document.querySelector("#color").addEventListener("input", aqua);
};
