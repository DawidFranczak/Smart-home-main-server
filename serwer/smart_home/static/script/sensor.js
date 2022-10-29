function add_sensor_button() {
  const as = document.querySelector(".select-sensor");
  const asb = document.querySelector("#add_sensor_button");
  const s = document.getElementById("save");
  const b = document.getElementById("back");
  const adb = document.getElementById("add_del_button");
  const fas = document.getElementById("f_add_sensor");

  if (as.style.display == "none") {
    as.style.display = "block";
    asb.style.display = "none";
    s.addEventListener("click", fadd_sensor);
    b.addEventListener("click", add_sensor_button);
    adb.removeEventListener("click", add_del_button);
    fas.removeEventListener("click", add_sensor_button);
  } else {
    as.style.display = "none";
    asb.style.display = "block";
    s.removeEventListener("click", fadd_sensor);
    b.removeEventListener("click", add_sensor_button);
    document.querySelector("#response").innerHTML = "";
    adb.addEventListener("click", add_del_button);
    fas.addEventListener("click", add_sensor_button);
  }
  if (document.querySelector(".sensor_del_but").style.display == "")
    add_del_button();
}

async function fadd_sensor() {
  let name = document.querySelector("#sensor_name").value;
  let fun = document.querySelectorAll(".sen-fun");
  let id;

  document.querySelector("#response").innerHTML = "Trwa dodawanie czujnika";

  if (name != "") {
    fun.forEach((s) => {
      if (s.checked) {
        fun = s.value;
        if (fun == "uid") {
          document.querySelectorAll(".sen-fun-uid").forEach((c) => {
            if (c.checked) {
              id = c.id;
            }
          });
          if (id === undefined) {
            document.querySelector("#response").innerHTML = "Wybierz czujnik";
            return false;
          }
        }
      }
    });
    const dict = { action: "add", name: name, fun: fun, id: id };
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
      input.setAttribute("class", "sensor_del_but");

      pName.setAttribute("class", "sensor_name");
      pName.innerHTML = name;

      pFun.setAttribute("class", "sensor_fun");

      div.setAttribute("class", "sensor");
      div.appendChild(pName);

      switch (fun) {
        case "temp":
          pFun.innerHTML = "Temperatura";
          div.appendChild(pFun);
          div.appendChild(input);
          document.getElementById("add_sensor_temp_container").appendChild(div);
          break;
        case "sunblind":
          pFun.innerHTML = "Roleta";
          div.appendChild(pFun);
          div.appendChild(input);
          document.getElementById("add_rolety_container").appendChild(div);
          break;
        case "light":
          pFun.innerHTML = "Światło";
          div.appendChild(pFun);
          div.appendChild(input);
          document.getElementById("add_swiatlo_container").appendChild(div);
          break;
        case "aqua":
          pFun.innerHTML = "Akwarium";
          div.appendChild(pFun);
          div.appendChild(input);
          document.getElementById("add_aqua_container").appendChild(div);
          break;
        case "rfid":
          pFun.innerHTML = "RFID";
          div.appendChild(pFun);
          div.appendChild(input);
          document.getElementById("add_rfid_container").appendChild(div);
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
          document.querySelector(".select-rfid").appendChild(ul);
          break;
        case "uid":
          pFun.innerHTML = "Karta/brelok";
          input.setAttribute("id", "card " + dataRep["id"]);
          div.appendChild(pFun);
          div.appendChild(input);
          document.getElementById("add_rfid_container").appendChild(div);
          break;
        case "btn":
          pFun.innerHTML = "Przycisk";
          div.appendChild(pFun);
          div.appendChild(input);
          document.getElementById("add_btn_container").appendChild(div);
          break;
        case "lamp":
          pFun.innerHTML = "Lampy";
          div.appendChild(pFun);
          div.appendChild(input);
          document.getElementById("add_lamp_container").appendChild(div);
          break;
        case "stairs":
          pFun.innerHTML = "Schody";
          div.appendChild(pFun);
          div.appendChild(input);
          document.getElementById("add_stairs_container").appendChild(div);
          break;
      }
      document.getElementById("response").innerHTML = dataRep["response"];
    } else document.getElementById("response").innerHTML = dataRep["response"];
  } else {
    document.getElementById("response").innerHTML = "Brak nazwy";
  }
}

function add_del_button() {
  document.querySelectorAll(".sensor_del_but").forEach((d) => {
    if (d.style.display == "none") {
      d.style.display = "";
    } else {
      d.style.display = "none";
    }
  });
}

async function delete_sensor(e) {
  if (e.target.type == "image") {
    const del = e.target.parentElement;
    dict = { id: e.target.id };
    dataRep = await sendData("DELETE", dict);
    if (dataRep["response"] == "permission") {
      del.remove();
      document.querySelectorAll(".sen-fun-uid").forEach((u) => {
        if (u.id == e.target.id) {
          u.parentElement.remove();
        }
      });
    }
  }
}

function search() {
  let sensors = document.getElementsByClassName("sensor_name");
  let search = document.getElementById("search").value.toLowerCase();
  for (let sensor of sensors) {
    if (sensor.innerHTML.toLowerCase().indexOf(search.toLowerCase()) > -1) {
      sensor.parentElement.style.display = "";
    } else {
      sensor.parentElement.style.display = "none";
    }
  }
}

function showRfid(e) {
  let rfid = document.querySelector(".select-rfid");
  if (e.target.type == "radio" && e.target.value == "uid")
    rfid.style.display = "block";
  else if (e.target.type == "radio" && e.target.value != "uid")
    rfid.style.display = "none";
}

window.onload = function () {
  document
    .querySelector("#f_add_sensor")
    .addEventListener("click", add_sensor_button);
  document
    .querySelector("#add_del_button")
    .addEventListener("click", add_del_button);
  document.querySelector("#search").addEventListener("keyup", search);
  document
    .querySelector(".sensor-container")
    .addEventListener("click", delete_sensor);
  document.querySelector(".select-sensor").addEventListener("click", showRfid);
};
