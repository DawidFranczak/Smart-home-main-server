function calibration(e) {
    let mess = document.getElementById("message");
    switch (e.type) {
      case "mousedown":
        dict = { action: this.id };
        sendData('POST',dict);
        break;
      case "mouseup":
        dict = { action: "stop" };
        sendData('POST',dict);
        break;
      case "click":
        if (this.value == "Zakończ") {
          dict = { action: "end" };
          sendData('POST',dict);
          document.getElementById("clbBtn").style.display = "none";
          document.getElementById("confBtn").style.display = "";
          mess.innerHTML = "Czy chcesz powtórzyć kalibrację ?";
          break;
        } else if (this.value == "Tak") {
          dict = { action: "calibration" };
          sendData('POST',dict);
          document.getElementById("clbBtn").style.display = "";
          document.getElementById("confBtn").style.display = "none";
          document.getElementById("save").value = "Zapisz";
          mess.innerHTML =
            "Zaczynamy kalibrację, proszę zasunąć roletę i nacisnąć przycisk 'zapisz'";
          break;
        }
        dict = { action: "save" };
        sendData('POST',dict);
        document.getElementById("save").value = "Zakończ";
        mess.innerHTML = "Teraz zasuń roletę i naciśnij przycisk 'zakończ'";
        break;
    }
  }

window.onload = function(){
  document.getElementById("up").addEventListener("mousedown", calibration);
  document.getElementById("up").addEventListener("mouseup", calibration);
  document.getElementById("down").addEventListener("mousedown", calibration);
  document.getElementById("down").addEventListener("mouseup", calibration);
  document.getElementById("save").addEventListener("click", calibration);
  document.getElementById("rep").addEventListener("click", calibration);
}