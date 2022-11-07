const addDelButton = () => {
  document.querySelectorAll("#sensor-del-button").forEach((sensor) => {
    sensor.classList.toggle('active-block');
  });
}

const addSensorSelectButton = ()=> {

  const selectSensor = document.querySelector("#select-sensor");
  const addSensorButton = document.querySelector("#add-sensor-button");
  const save = document.querySelector("#save");
  const back = document.querySelector("#back");
  const addSensorDelButton = document.querySelector("#add-del-button");
  const addSensor = document.querySelector("#add-sensor");

  if (selectSensor.style.display == "none") {
    selectSensor.style.display = "block";
    addSensorButton.style.display = "none";
    save.addEventListener("click", addSensorSave);
    back.addEventListener("click", addSensorSelectButton);
    addSensorDelButton.removeEventListener("click", addDelButton);
    addSensor.removeEventListener("click", addSensorSelectButton);

  } else {
    document.querySelector("#response").innerHTML = "";
    selectSensor.style.display = "none";
    addSensorButton.style.display = "block";
    save.removeEventListener("click", addSensorSave);
    back.removeEventListener("click", addSensorSelectButton);
    addSensorDelButton.addEventListener("click", addDelButton);
    addSensor.addEventListener("click", addSensorSelectButton);
  }

  document.querySelector("#sensor-del-button").classList.forEach(c =>{
    if(c === 'active-block'){
      addDelButton()
      return;
    }
  })
}

const addSensorSave = async () => {
  const name = document.querySelector("#sensor-name-add").value;
  const sensorFunctions = document.querySelectorAll("#sensor-fun");
  let id;
  let newSensorFunction;

  document.querySelector("#response").innerHTML = "Trwa dodawanie czujnika";

  if (name != "") {
    sensorFunctions.forEach((sensor) => {
      if (sensor.checked) {
        newSensorFunction = sensor.value;
        return;
      }});
    if (newSensorFunction === "uid") {
      document.querySelectorAll("#sensor-fun-uid").forEach((sensor) => {
        if (sensor.checked) {
          id = sensor.id;
          return;
        }});
      if (id === undefined) {
        document.querySelector("#response").innerHTML = "Wybierz czujnik";
      }
    }

    const dict = { action: "add", name: name, fun: newSensorFunction, id: id };
    dataRep = await sendData("POST", dict);

    if (dataRep["response"] == "Udało sie dodać czujnik") {

      const div = document.createElement("ul");
      const pName = document.createElement("p");
      const pFun = document.createElement("p");
      const input = document.createElement("input");

      input.setAttribute("type", "image");
      input.setAttribute("src", "/static/images/cross.png");
      input.setAttribute("id", dataRep["id"]);
      input.setAttribute("style", "display:none");
      input.setAttribute("class", "sensor-del-but");

      pName.setAttribute("class", "sensor-name");
      pName.setAttribute("id", "sensor-name");
      pName.innerHTML = name;

      pFun.setAttribute("class", "sensor-fun");

      div.setAttribute("class", "sensor");
      div.appendChild(pName);

      switch (newSensorFunction) {
        case "temp":
          pFun.innerHTML = "Temperatura";
          div.appendChild(pFun);
          div.appendChild(input);
          document.getElementById("add-sensor-temp-container").appendChild(div);
          break;
        case "sunblind":
          pFun.innerHTML = "Roleta";
          div.appendChild(pFun);
          div.appendChild(input);
          document.getElementById("add-rolety-container").appendChild(div);
          break;
        case "light":
          pFun.innerHTML = "Światło";
          div.appendChild(pFun);
          div.appendChild(input);
          document.getElementById("add-swiatlo-container").appendChild(div);
          break;
        case "aqua":
          pFun.innerHTML = "Akwarium";
          div.appendChild(pFun);
          div.appendChild(input);
          document.getElementById("add-aqua-container").appendChild(div);
          break;
        case "rfid":
          pFun.innerHTML = "RFID";
          div.appendChild(pFun);
          div.appendChild(input);
          document.getElementById("add-rfid-container").appendChild(div);
          const radio = document.createElement("input");
          radio.setAttribute("type", "radio");
          radio.setAttribute("name", "rfid");
          radio.setAttribute("class", "sen-fun-uid");
          radio.setAttribute("value", "uid");
          radio.setAttribute("id", dataRep["id"]);

          const ul = document.createElement("ul");
          const label = document.createElement("label");
          label.setAttribute("for", "uid");
          label.innerHTML = name;
          ul.appendChild(radio);
          ul.appendChild(label);
          document.querySelector("#select-rfid").appendChild(ul);
          break;
        case "uid":
          pFun.innerHTML = "Karta/brelok";
          input.setAttribute("id", "card " + dataRep["id"]);
          div.appendChild(pFun);
          div.appendChild(input);
          document.getElementById("add-rfid-container").appendChild(div);
          break;
        case "btn":
          pFun.innerHTML = "Przycisk";
          div.appendChild(pFun);
          div.appendChild(input);
          document.getElementById("add-btn-container").appendChild(div);
          break;
        case "lamp":
          pFun.innerHTML = "Lampy";
          div.appendChild(pFun);
          div.appendChild(input);
          document.getElementById("add-lamp-container").appendChild(div);
          break;
        case "stairs":
          pFun.innerHTML = "Schody";
          div.appendChild(pFun);
          div.appendChild(input);
          document.getElementById("add-stairs-container").appendChild(div);
          break;
      }
      document.getElementById("response").innerHTML = dataRep["response"];

    } else document.getElementById("response").innerHTML = dataRep["response"];
  } else {
    document.getElementById("response").innerHTML = "Brak nazwy";
  }
}

const deleteSensor= async (e) => {
  if (e.target.type == "image") {
    const sensorDelete = e.target.parentElement;
    const sensorId = e.target.placeholder;
    dict = { 
      id: sensorId
    };
    dataRep = await sendData("DELETE", dict);
    if (dataRep["response"] == "permission") {
      sensorDelete.remove();
      // document.querySelectorAll(".sensor-fun-uid").forEach((u) => {
      //   if (u.id == e.target.id) {
      //     u.parentElement.remove();
      //   }
      // });
    }
  }
}

function search() {
  const sensors = document.querySelectorAll("#sensor-name");
  const search = document.querySelector("#search").value.toLowerCase();
  console.log(search)
  console.log(sensors)

  for (let sensor of sensors) {
    if (sensor.innerHTML.toLowerCase().indexOf(search.toLowerCase()) > -1) {
      sensor.parentElement.style.display = "";
    } else {
      sensor.parentElement.style.display = "none";
    }
  }
}

function showRfid(e) {
  let rfid = document.querySelector("#select-rfid");
  const target = e.target;
  if (target.type == "radio" && target.value == "uid")
    rfid.classList.add('active-block');
  else if (target.type == "radio" && target.value != "uid")
    rfid.classList.remove('active-block');

}

window.onload = function () {
  document
    .querySelector("#add-sensor")
    .addEventListener("click", addSensorSelectButton);
  document
    .querySelector("#add-del-button")
    .addEventListener("click", addDelButton);
  document.querySelector("#search").addEventListener("keyup", search);
  document
    .querySelector(".sensor-container")
    .addEventListener("click", deleteSensor);
  document.querySelector(".select-sensor").addEventListener("click", showRfid);
};
