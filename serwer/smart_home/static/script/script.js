// function get_sensor(title) {
//   switch (title){
//     case "Czujniki":
//       // document.querySelector('#f_add_sensor').addEventListener("click", add_sensor_button);
//       // document.querySelector('#add_del_button').addEventListener("click", add_del_button);
//       // document.querySelector('#search').addEventListener("keyup", search);
//       // document.querySelector('.sensor-container').addEventListener('click',delete_sensor);
//       // document.querySelector('.add-sensor').addEventListener('click',showRfid);
//       break;
      
//     case "Rolety":
//       // document.querySelector('#calibration').addEventListener("click",() =>{
//       // document.querySelectorAll(".calBtn").forEach( btn =>{
//       //     if (btn.style.display === "") btn.style.display = "none";
//       //     else btn.style.display = "";
//       //   })
//       // });
//       // document.querySelectorAll('.slider').forEach(s =>{
//       //   s.addEventListener("mousedown", sunblind);
//       //   s.addEventListener("mouseup", sunblind);
//       // })
      
//       break;
//     case "Światło":
//       // document.querySelectorAll('.button').forEach(b=>{
//       //   b.addEventListener("click", change_light);
//       // });
//       break;
//     case "Akwarium":
//       // document.getElementsByClassName('.button').forEach(b=>{
//       //   b.addEventListener("click", select_aqua);
//       // });
//       // document.getElementById("color").addEventListener("input", aqua);
//       // document.getElementById("ledButton").addEventListener("click", aqua);
//       // document.getElementById("fluoLampButton").addEventListener("click", aqua);
//       // document.getElementById("mode").addEventListener("click", aqua);
//       // document.getElementById("modeLedButton").addEventListener("click", aqua);
//       // document
//       //   .getElementById("modeFluoLampButton")
//       //   .addEventListener("click", aqua);
//       break;
//     case "Kalibracja":
//       // document.getElementById("up").addEventListener("mousedown", calibration);
//       // document.getElementById("up").addEventListener("mouseup", calibration);
//       // document.getElementById("down").addEventListener("mousedown", calibration);
//       // document.getElementById("down").addEventListener("mouseup", calibration);
//       // document.getElementById("save").addEventListener("click", calibration);
//       // document.getElementById("rep").addEventListener("click", calibration);
//       break;
//     case "Schody":
//       // document.querySelectorAll(".button").forEach(btn => btn.addEventListener('click',select_stairs));
//       break;
//     case 'RPL':
//       // document.querySelector('.rpl-containers').addEventListener('click',select_rpl);  
//       // document.querySelectorAll('#lamp').forEach(l =>{
//       //   l.addEventListener('click',select_rpl)
//       // })
//   }
// }

function test(e){
  console.log('=====================')
  console.log(e)
  console.log('=====================')

}


function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    var cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      let cookie = cookies[i].trim();
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}


async function sendData(method,_dict) {
  var csrftoken = getCookie("csrftoken");
  const data = await fetch(window.location.href,{
    method: method,
    headers: {'Content-Type':'application/json',
                "X-CSRFToken": csrftoken},
    body: JSON.stringify(_dict)
  })
//   try {
//     JSON.parse(data);
//     console.log(data)
// }
// catch (error) {
//     console.log('Error parsing JSON:', error, data);
// }
  return data.json();

}


const checkClock = (t) => {
  if(t<10) t = "0"+ t
  return t
}

const clock = () =>{
  const today = new Date();
  let h = today.getHours();
  let m = today.getMinutes();
  let s = today.getSeconds();
  h = checkClock(h);
  m = checkClock(m);
  s = checkClock(s);

  document.querySelector(".clock").innerHTML = "Czas serwera: " + h + ":" + m + ":" + s;
  setTimeout(clock,1000);
}


window.onload = function () {
  // const title = document.title;
  // get_sensor(title);
  // clock();
};
