function select_stairs(){
    let xhr = new XMLHttpRequest();
    xhr.open("POST", "/schody/", true);
    var csrftoken = getCookie("csrftoken");
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.setRequestHeader("X-CSRFToken", csrftoken);
    dict = { action: "get", id: this.placeholder };
    xhr.onload = function () {
      let dataRep = JSON.parse(this.responseText);
      console.log(dataRep)
      document.querySelector("#lightingTime").value = dataRep['lightTime'];
      document.querySelector("#brightness").value = dataRep['brightness'];
      document.querySelector("#step").value = dataRep['steps'];
      document.querySelector('#stairs_containers').placeholder = dataRep['sensor_id'];
      document.querySelector('#stairs_containers').setAttribute("style","display:block")
      if (dataRep["mode"]) document.querySelector('#stairs-btn').value = "Wyłącz";
      else document.querySelector('#stairs-btn').value = "Włącz";
      document.querySelectorAll('.stairs-btn').forEach(btn => {
        btn.addEventListener('click',settings_stairs);
      })
  
    };
    xhr.send(JSON.stringify(dict));
  }
  
  function settings_stairs(){
    console.log(this.placeholder)
    id = document.querySelector('#stairs_containers').placeholder;
    switch(this.placeholder){
      case "stairs-btn":
        dict={'action':'change-stairs',
              'id':id}
              console.log(dict)
        if(this.value == "Włącz") this.value = "Wyłącz";
        else this.value = "Włącz"
        sendData('POST',dict)
        break;
      case "step":
        let step = document.querySelector('#step').value;
        if (step<1) {
          step = 1;
          document.querySelector('#step').value = 1;
        }
        if (step<1) step = 1;
        dict={'action':'set-step',
              'id':id,
              'step': step}
        console.log(dict)
        sendData('POST',dict)
        break;
      case "brightness":
        let brightness = document.querySelector('#brightness').value;
        if(brightness>100) brightness = 100;
        else if(brightness<0) brightness = 0;
        document.querySelector('#brightness').value = brightness;
        dict={'action':'set-brightness',
              'id':id,
              'brightness': brightness}
        console.log(dict)
        sendData('POST',dict)
        break;
      case "lightingTime":
        let lightTime = document.querySelector('#lightingTime').value
        if(lightTime <0 ) {
          lightTime = 0;
          document.querySelector('#lightingTime').value = 0
        }
        dict={'action':'set-lightingTime',
              'id':id,
              'lightingTime': lightTime}
        console.log(dict)
        sendData('POST',dict)
  
        break;
    }
  
  }

  window.onload = function(){
    document.querySelectorAll(".button").forEach(btn => btn.addEventListener('click',select_stairs));
  }