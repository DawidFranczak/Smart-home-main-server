function translation(){
  const LANG = window.navigator.language;
  if (LANG === "pl-PL"){
      let TRANSLATE = {
          "ON" : "Włącz",
          "OFF" : "Wyłącz",
          "MODE_MAUAL" : "Ręczny",
          "MODE_AUTO" : "Automat",
          "HOUR_ERROR" : "Brak jednej godziny",
          "SELECT": "Wybrano ",
      }
  return TRANSLATE
  }else{
      let TRANSLATE = {
          "ON" : "ON",
          "OFF" : "OFF",
          "MODE_MAUAL" : "Manual",
          "MODE_AUTO" : "Auto",
          "HOUR_ERROR" : "Without one hour",
          "SELECT": "Selected ",

      }
  return TRANSLATE
  }
}
const selectAqua = async (e) => {
  /* The function getting
     the settings of the operating mode,
     lighting time of fluorescent lamps and LEDs 
  */
  const selectButton = e.target.type;
  const aquariumMessage = document.querySelector("#message");
  aquariumMessage.innerHTML = "";

  if (selectButton != "submit") return;

  const aquarium = e.target;

  settings = await fetch(`/api/aquarium/${aquarium.id}`);
  settings = await settings.json();
  tr = translation()

  const containerAqua = document.querySelector("#containers-aqua");
  containerAqua.classList.add("Containers-aqua--active");
  containerAqua.setAttribute("placeholder", aquarium.id);

  document.querySelector("#color").value = settings["color_rgb"];
  document.querySelector("#fluolamp-start").value = settings["fluo_start"];
  document.querySelector("#fluolamp-stop").value = settings["fluo_stop"];
  document.querySelector("#led-start").value = settings["led_start"];
  document.querySelector("#led-stop").value = settings["led_stop"];
  document.querySelector("#select").innerHTML = tr["SELECT"] + aquarium.innerHTML;

  const mode = document.querySelector("#mode");
  const modeButton = document.querySelector("#mode-buttons");
  const settingsAqua = document.querySelector("#settings-aqua");

  if (settings["mode"]) {
    mode.innerHTML = tr["MODE_AUTO"];
    modeButton.classList.add("Containers-aqua__mode-buttons--active");
    settingsAqua.classList.remove("Containers-aqua__settings-aqua--active");
  } else {
    mode.innerHTML = tr["MODE_MAUAL"];
    modeButton.classList.remove("Containers-aqua__mode-buttons--active");
    settingsAqua.classList.add("Containers-aqua__settings-aqua--active");
  }

  const modeFluoLampButton = document.querySelector("#mode-button-fluolamp");
  const modeLedButton = document.querySelector("#mode-button-led");

  modeFluoLampButton.innerHTML = settings["fluo_mode"] ? tr["OFF"] : tr["ON"];
  modeLedButton.innerHTML = settings["led_mode"] ? tr["OFF"] : tr["ON"];

  document.querySelector("#containers-aqua").addEventListener("click", aqua);
  document.querySelector("#color").addEventListener("input", aqua);
};

const aqua = async (e) => {
  /* This function allow to change the aquarium settings */

  const target = e.target;
  if (target.type === "submit" || target.id === "color") {
    document.querySelector("#message").innerHTML = "";

    let dict = {};
    const id = document
      .querySelector("#containers-aqua")
      .getAttribute("placeholder");
    const action = target.id;

    switch (action) {
      case "color":
        const aqua = document.querySelector("#color");
        const color = aqua.value.substring(4, aqua.value.length - 1).split(",");

        const [r, g, b] = color;
        dict = {
          action: "changeRGB",
          r: r,
          g: g,
          b: b,
          id: id,
        };
        break;
      case "led-button":
        const ledStart = document.querySelector("#led-start");
        const ledStop = document.querySelector("#led-stop");

        if (ledStart.value === "" || ledStop.value === "") {
          document.querySelector("#led-mess").innerHTML = tr["HOUR_ERROR"];
        } else {
          dict = {
            action: "changeLedTime",
            ledStart: ledStart.value,
            ledStop: ledStop.value,
            id: id,
          };
        }
        break;
      case "fluolamp-button":
        const fluoLampStart = document.querySelector("#fluolamp-start");
        const fluoLampStop = document.querySelector("#fluolamp-stop");

        if (fluoLampStart.value === "" || fluoLampStop.value === "") {
          document.querySelector("fluolamp-mess").innerHTML =
            "Brak jednej godziny";
        } else {
          dict = {
            action: "changeFluoLampTime",
            fluoLampStart: fluoLampStart.value,
            fluoLampStop: fluoLampStop.value,
            id: id,
          };
        }
        break;
      case "mode":
        let mode = false;
        const modeButton = e.target;
        if (modeButton.innerHTML === tr["MODE_MAUAL"]) {
          mode = true;
          modeButton.innerHTML = tr["MODE_AUTO"];
          document
            .querySelector("#mode-buttons")
            .classList.add("Containers-aqua__mode-buttons--active");
          document
            .querySelector("#settings-aqua")
            .classList.remove("Containers-aqua__settings-aqua--active");
        } else {
          modeButton.innerHTML = tr["MODE_MAUAL"];
          document
            .querySelector("#mode-buttons")
            .classList.remove("Containers-aqua__mode-buttons--active");
          document
            .querySelector("#settings-aqua")
            .classList.add("Containers-aqua__settings-aqua--active");
        }

        dict = {
          action: "changeMode",
          mode: mode,
          id: id,
        };

        data = await sendData("POST", dict);
        data = await data.json()

        const modeFluolampButton = document.querySelector(
          "#mode-button-fluolamp"
        );

        const modeLedButton = document.querySelector("#mode-button-led");

        modeFluolampButton.innerHTML = data["fluo"] ? tr["OFF"] : tr["ON"];
        modeLedButton.innerHTML = data["led"] ? tr["OFF"] : tr["ON"];

        break;
      case "mode-button-fluolamp":
        let valueFluolamp = false;
        const fluolampMode = e.target;
        if (fluolampMode.innerHTML === tr["ON"]) {
          fluolampMode.innerHTML = tr["OFF"];
          valueFluolamp = true;
        } else {
          fluolampMode.innerHTML = tr["ON"];
        }

        dict = {
          action: "changeFluoLampState",
          value: valueFluolamp,
          id: id,
        };
        break;
      case "mode-button-led":
        let valueLed = false;
        const ledMode = e.target;

        if (ledMode.innerHTML === tr["ON"]) {
          ledMode.innerHTML = tr["OFF"];
          valueLed = true;
        } else {
          ledMode.innerHTML = tr["ON"];
        }
        dict = {
          action: "changeLedState",
          value: valueLed,
          id: id,
        };
        break;
    }
    let rep = await sendData("POST", dict);
    rep = await rep.json()
    if (rep["message"] != undefined) {
      document.querySelector("#message").innerHTML = rep["message"];
    }
  }
};

document.querySelector("#select-aqua").addEventListener("click", selectAqua);
