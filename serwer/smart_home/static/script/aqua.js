async function select_aqua() {
  id = this.id;
  settings = await fetch(`/api/akwarium/${id}`)
  settings = await settings.json()
  console.log(settings)

  document
    .getElementById("aqua_containers")
    .setAttribute("style", "display:block");
  document.getElementById("aqua_containers").setAttribute("placeholder", id);

    if (settings["mode"] == false) {
      document.getElementById("mode").value = "Ręczny";
      document.getElementById("modeButtons").style.display = "none";
      document.getElementById("settings_aqua").style.display = "";
    } else {
      document.getElementById("mode").value = "Automat";
      document.getElementById("modeButtons").style.display = "";
      document.getElementById("settings_aqua").style.display = "none";
    }

    if (settings["fluo_mode"] === true)
      document.getElementById("modeFluoLampButton").value = "Wyłącz";
    else document.getElementById("modeFluoLampButton").value = "Włącz";

    if (settings["led_mode"] === true)
      document.getElementById("modeLedButton").value = "Wyłącz";
    else document.getElementById("modeLedButton").value = "Włącz";

    if (settings["fluo_start"] != "" && settings["fluo_start"] != null) {
      document.getElementById("fluoLampStart").value = settings["fluo_start"];
    }

    if (settings["fluo_stop"] != "" && settings["fluo_stop"] != null) {
      document.getElementById("fluoLampStop").value = settings["fluo_stop"];
    }

    if (settings["led_start"] != "" && settings["led_start"] != null) {
      document.getElementById("ledStart").value = settings["led_start"];
    }

    if (settings["led_stop"] != "" && settings["led_stop"] != null) {
      document.getElementById("ledStop").value = settings["led_stop"];
    }
}

async function aqua() {
  console.log(this)
  if (this.id === "color") {
    let aqua = document.getElementById("color");
    let color = aqua.value.substring(4, aqua.value.length - 1).split(",");
    this.oninput = function () {
      let dict = {
        action: "changeRGB",
        r: color[0],
        g: color[1],
        b: color[2],
        id: document
          .querySelector("#aqua_containers")
          .getAttribute("placeholder"),
      };
      sendData('POST',dict);
    };
  } else if (this.id === "ledButton") {
    let ledStart = document.getElementById("ledStart").value;
    let ledStop = document.getElementById("ledStop").value;

    if (ledStart === "" || ledStop === "") {
      document.getElementById("ledMess").innerHTML = "Brak jednej godziny";
    } else {
      let dict = {
        action: "changeLedTime",
        ledStart: ledStart,
        ledStop: ledStop,
        id: document
          .getElementById("aqua_containers")
          .getAttribute("placeholder"),
      };
      sendData('POST',dict);
    }
  } else if (this.id === "fluoLampButton") {
    let fluoLampStart = document.getElementById("fluoLampStart").value;
    let fluoLampStop = document.getElementById("fluoLampStop").value;
    if (fluoLampStart === "" || fluoLampStop === "") {
      document.getElementById("fluoLampMess").innerHTML = "Brak jednej godziny";
    } else {
      let dict = {
        action: "changeFluoLampTime",
        fluoLampStart: fluoLampStart,
        fluoLampStop: fluoLampStop,
        id: document
          .getElementById("aqua_containers")
          .getAttribute("placeholder"),
      };
      sendData('POST',dict);
    }
  } else if (this.id === "mode") {
    if (this.value === "Ręczny") {
      var mode = true;
      this.value = "Automat";
      document.getElementById("modeButtons").style.display = "";
      document.getElementById("settings_aqua").style.display = "none";
    } else {
      mode = false;
      this.value = "Ręczny";
      document.getElementById("modeButtons").style.display = "none";
      document.getElementById("settings_aqua").style.display = "";
    }
    let dict = {
      action: "changeMode",
      mode: mode,
      id: document
        .getElementById("aqua_containers")
        .getAttribute("placeholder"),
    };
    data = await sendData('POST',dict);
    console.log(data)
    
    if (data['fluo']) document.querySelector('#modeFluoLampButton').value = 'Wyłącz';
    else document.querySelector('#modeFluoLampButton').value = 'Włącz';

    if (data['led']) document.querySelector('#modeLedButton').value = 'Wyłącz';
    else document.querySelector('#modeLedButton').value = 'Włącz';

  } else if (this.id === "modeFluoLampButton") {
    if (this.value === "Włącz") {
      document.getElementById("modeFluoLampButton").value = "Wyłącz";
      var value = true;
    } else {
      document.getElementById("modeFluoLampButton").value = "Włącz";
      var value = false;
    }
    dict = {
      action: "changeFluoLampState",
      value: value,
      id: document
        .getElementById("aqua_containers")
        .getAttribute("placeholder"),
    };
    sendData('POST',dict);
  } else if (this.id === "modeLedButton") {
    if (this.value === "Włącz") {
      document.getElementById("modeLedButton").value = "Wyłącz";
      var value = true;
    } else {
      document.getElementById("modeLedButton").value = "Włącz";
      var value = false;
    }
    dict = {
      action: "changeLedState",
      value: value,
      id: document
        .getElementById("aqua_containers")
        .getAttribute("placeholder"),
    };
    sendData('POST',dict);
  }
}

window.onload = function(){
  document.querySelectorAll('.button').forEach(b=>{
    b.addEventListener("click", select_aqua);
  });
  document.querySelector("#color").addEventListener("input", aqua);
  document.querySelector("#ledButton").addEventListener("click", aqua);
  document.querySelector("#fluoLampButton").addEventListener("click", aqua);
  document.querySelector("#mode").addEventListener("click", aqua);
  document.querySelector("#modeLedButton").addEventListener("click", aqua);
  document
    .querySelector("#modeFluoLampButton")
    .addEventListener("click", aqua);
}