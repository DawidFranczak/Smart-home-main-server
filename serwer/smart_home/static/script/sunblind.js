function sunblind(e) {
    let p = document.getElementById(this.placeholder);
    switch (e.type) {
      case "mousedown":
        this.oninput = function () {
          p.innerHTML = this.value;
        };
        break;
      case "mouseup":
        let dict = { action: "set", value: this.value, id: this.placeholder };
        sendData('POST',dict);
    }
  }

window.onload = function(){
  document.querySelector('#calibration').addEventListener("click",() =>{
    document.querySelectorAll(".calBtn").forEach( btn =>{
        if (btn.style.display === "") btn.style.display = "none";
        else btn.style.display = "";
      })
    });
    document.querySelectorAll('.slider').forEach(s =>{
      s.addEventListener("mousedown", sunblind);
      s.addEventListener("mouseup", sunblind);
    })
}