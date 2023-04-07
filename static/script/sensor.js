const addDelButton = () => {
  document.querySelectorAll("#sensor-del-button").forEach((sensor) => {
    sensor.classList.toggle("Sensor-container__ul__sensor__del-button--active");
  });
};

const sensorSelect = (e) => {
  const element = e.target;
  switch (element.type) {
    case "radio":
      const rfid = document.querySelector("#select-rfid");
      if (element.value === "uid" || element.value === "card-uid")
        rfid.classList.add("Sensor-add__select__select-rfid--active");
      else rfid.classList.remove("Sensor-add__select__select-rfid--active");
      break;

    case "submit":
      if (element.value === "save") sensorSave();
      else {
        const selectSensor = document.querySelector("#select-sensor");
        const buttons = document.querySelector("#add-sensor-button");

        selectSensor.removeEventListener("click", sensorSelect);
        selectSensor.classList.remove("Sensor-add--active");

        buttons.classList.add("Add-sensor-button--active");
        buttons.addEventListener("click", selectButton);
      }
      break;
  }
};

const selectButton = (e) => {
  const button = e.target;
  switch (button.id) {
    case "add-sensor":
      const buttons = document.querySelector("#add-sensor-button");

      buttons.removeEventListener("click", selectButton);
      addSensorSelect();
      break;

    case "add-del-button":
      addDelButton();
      break;
  }
};

const addSensorSelect = () => {
  const selectSensor = document.querySelector("#select-sensor");
  const buttons = document.querySelector("#add-sensor-button");
  const respnse = document.querySelector("#response");

  selectSensor.addEventListener("click", sensorSelect);
  selectSensor.classList.add("Sensor-add--active");

  buttons.classList.remove("Add-sensor-button--active");

  respnse.innerHTML = "";

  document.querySelector("#sensor-del-button").classList.forEach((c) => {
    if (c === "Sensor-container__ul__sensor__del-button--active") {
      addDelButton();
      return;
    }
  });
};

const sensorSave = async () => {
  const name = document.querySelector("#sensor-name-add").value;
  const sensorFunctions = document.querySelectorAll("#sensor-fun");
  let id;
  let newSensorFunction;

  document.querySelector("#response").innerHTML = "Trwa dodawanie czujnika";

  if (name === "") {
    document.getElementById("response").innerHTML = "Brak nazwy";
    return;
  }

  sensorFunctions.forEach((sensor) => {
    if (sensor.checked) {
      newSensorFunction = sensor.value;
      return;
    }
  });
  if (newSensorFunction === "uid") {
    document.querySelectorAll("#sensor-fun-uid").forEach((sensor) => {
      if (sensor.checked) {
        id = sensor.placeholder;
        return;
      }
    });
    if (id === undefined) {
      document.querySelector("#response").innerHTML = "Wybierz czujnik";
      return;
    }
  }

  const dict = {
    action: "add",
    name: name,
    fun: newSensorFunction,
    id: id,
  };
  dataRep = await sendData("POST", dict,"add");
  const status = dataRep['status']
  dataRep = await dataRep.json()
  
  if (status === 201) {
    const parent = document.createElement("ul");
    const pName = document.createElement("p");
    const pFun = document.createElement("img");
    const input = document.createElement("input");

    input.setAttribute("type", "image");
    input.setAttribute("id", "sensor-del-button");
    input.setAttribute("placeholder", dataRep["id"]);
    input.setAttribute("src", "/static/images/cross.png");
    input.setAttribute("class", "Sensor-container__ul__sensor__del-button");

    pName.innerHTML = name;
    pName.setAttribute("id", "sensor-name");
    pName.setAttribute("class", "Sensor-container__ul__sensor__name");

    pFun.setAttribute("class", "Sensor-container__ul__sensor__sensor-img");

    parent.appendChild(pName);
    parent.appendChild(pFun);
    parent.appendChild(input);
    parent.setAttribute("class", "Sensor-container__ul__sensor");

    switch (newSensorFunction) {
      case "temp":
        pFun.setAttribute("src", "/static/images/temp.png");
        pFun.setAttribute("alt", "Czujnik temperatury");
        document
          .querySelector("#add-sensors-temp-container")
          .appendChild(parent);
        break;
      case "sunblind":
        pFun.setAttribute("src", "/static/images/sunblind.png");
        pFun.setAttribute("alt", "Roleta");
        document.querySelector("#add-sunblinds-container").appendChild(parent);
        break;
      case "light":
        pFun.setAttribute("src", "/static/images/lamp.png");
        pFun.setAttribute("alt", "Światło");
        document.querySelector("#add-lights-container").appendChild(parent);
        break;
      case "aqua":
        pFun.setAttribute("src", "/static/images/aqua.png");
        pFun.setAttribute("alt", "Akwarium");
        document.querySelector("#add-aquas-container").appendChild(parent);
        break;
      case "rfid":
        pFun.setAttribute("src", "/static/images/sensor-rfid.png");
        pFun.setAttribute("alt", "Czytnik");
        document.querySelector("#add-rfids-container").appendChild(parent);

        const radio = document.createElement("input");
        radio.setAttribute("type", "radio");
        radio.setAttribute("name", "rfid");
        radio.setAttribute("value", "uid");
        radio.setAttribute("id", dataRep["id"]);
        radio.setAttribute("class", "sen-fun-uid");

        const div = document.createElement("div");
        const label = document.createElement("label");

        label.innerHTML = name;
        label.setAttribute("for", "uid");

        ul.appendChild(radio);
        ul.appendChild(label);
        document.querySelector("#select-rfid").appendChild(div);
        break;

      case "uid":
        pFun.setAttribute("alt", "Akwarium");
        pFun.setAttribute("src", "/static/images/aqua.png");

        input.setAttribute("id", "card " + dataRep["id"]);
        document.querySelector("#add-rfid-container").appendChild(parent);
        break;

      case "btn":
        pFun.setAttribute("alt", "Przycisk");
        pFun.setAttribute("src", "/static/images/redbutton.png");

        document.querySelector("#add-btns-container").appendChild(parent);
        break;

      case "lamp":
        pFun.innerHTML = "Lampy";
        document.querySelector("#add-lamps-container").appendChild(parent);
        break;

      case "stairs":
        pFun.setAttribute("alt", "Schody");
        pFun.setAttribute("src", "/static/images/stairs.png");

        document.querySelector("#add-stairses-container").appendChild(parent);
        break;
    }
    document.querySelector("#response").innerHTML = dataRep["response"];
  } else document.querySelector("#response").innerHTML = dataRep["response"];
};

const search = () => {
  const sensors = document.querySelectorAll("#sensor-name");
  const search = document.querySelector("#search").value.toLowerCase();
  for (let sensor of sensors) {
    if (sensor.innerHTML.toLowerCase().indexOf(search.toLowerCase()) > -1) {
      sensor.parentElement.classList.remove(
        "Sensor-container__ul__sensor--search"
      );
    } else {
      sensor.parentElement.classList.add(
        "Sensor-container__ul__sensor--search"
      );
    }
  }
};

document
  .querySelector("#add-sensor-button")
  .addEventListener("click", selectButton);
document.querySelector("#search").addEventListener("keyup", search);
document
  .querySelector("#sensor-container")
  .addEventListener("click", deleteSensor);
