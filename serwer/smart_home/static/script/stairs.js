const selectStairs = async (e) => {

  if (e.target.type != 'submit') return;
  settings = await fetch(`/api/schody/${e.target.id}`);
  settings = await settings.json();

  document.querySelector('#stairs-error-message').innerHTML = '';
  document.querySelector("#lightingTime").value = settings["lightTime"];
  document.querySelector("#brightness").value = settings["brightness"];
  document.querySelector("#step").value = settings["steps"];

  const stairs = document.querySelector("#stairs-containers");
  const stairsBtn = document.querySelector("#stairs-button");

  stairs.placeholder = settings["sensor"];
  stairs.classList.add('Stairs-containers--active');
  stairs.addEventListener("click", settingsStairs);

  stairsBtn.innerHTML = settings["mode"] ? "Wyłącz" : "Włącz";

  document.querySelector("#mess").innerHTML =`Wybrano ${e.target.innerHTML}`; 
}

async function settingsStairs(e) {
  if (e.target.type == "submit") {
    id = document.querySelector("#stairs-containers").placeholder;
    document.querySelector('#stairs-error-message').innerHTML = '';
    switch (e.target.id) {
    case "stairs-button":
      dict = { 
        action: "change-stairs",
        id: id
       };

      this.value = this.value == "Włącz" ? "Wyłącz" : "Włącz";
      break;

    case "step":
      const step = document.querySelector("#step");

      if (step.value < 1) {
        step.value = 1;
      } else if (step.value > 4096){
        step.value = 4096;
      }

      dict = {
        action: "set-step",
        id: id,
        step: step.value
      };

      break;

    case "brightness":
      const brightness = document.querySelector("#brightness");

      if (brightness.value > 100) brightness.value = 100;
      else if (brightness.value < 0) brightness.value = 0;

      dict = { 
        action: "set-brightness",
        id: id,
      brightness: brightness.value
     };
      break;

    case "lightingTime":
      const lightTime = document.querySelector("#lightingTime");

      if (lightTime.value < 0) {
        lightTime.value = 0;
      }
      dict = { 
        action: "set-lightingTime",
        id: id,
        lightingTime: lightTime.value
       };
      break;
    }
    sendData("POST", dict);
  }
}

window.onload = function () {
  document
  .querySelector("#select-stairs")
  .addEventListener("click", selectStairs);
};
