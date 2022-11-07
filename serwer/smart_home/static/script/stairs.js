async function select_stairs() {
  settings = await fetch(`/api/schody/${this.id}`);
  settings = await settings.json();

  document.querySelector('.stairs-error-message').innerHTML = '';
 
  document.querySelector("#lightingTime").value = settings["lightTime"];
  document.querySelector("#brightness").value = settings["brightness"];
  document.querySelector("#step").value = settings["steps"];
  document.querySelector(".stairs_containers").id = settings["sensor"];

  document
    .querySelector(".stairs_containers")
    .setAttribute("style", "display:block");
    

  const stairsBtn = document.querySelector("#stairs-btn");

  stairsBtn.value = settings["mode"] ? "Wyłącz" : "Włącz";

  document
    .querySelector(".stairs_containers")
    .addEventListener("click", settings_stairs);

  document.querySelector(".mess").innerHTML =`Wybrano ${this.value}`; 
}

async function settings_stairs(e) {
  if (e.target.type == "button") {
    id = document.querySelector(".stairs_containers").id;
    document.querySelector('.stairs-error-message').innerHTML = '';

    switch (e.target.placeholder) {
    case "stairs-btn":
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
    .querySelectorAll(".button")
    .forEach((btn) => btn.addEventListener("click", select_stairs));
};
