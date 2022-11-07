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

async function sendData(method, _dict) {
  const csrftoken = getCookie("csrftoken");
  const data = await fetch(window.location.href, {
    method: method,
    headers: { "Content-Type": "application/json", "X-CSRFToken": csrftoken },
    body: JSON.stringify(_dict),
  });
  //   try {
  //     JSON.parse(data);
  //     console.log(data)
      
  // }
  // catch (error) {
  //     console.log('Error parsing JSON:', error, data);
  // }
  // if (data.json()){
  //   console.log(1)
  // }
  
  return data.json();
}

const checkClock = (t) => {
  if (t < 10) t = "0" + t;
  return t;
};

const clock = () => {
  const today = new Date();
  let h = today.getHours();
  let m = today.getMinutes();
  let s = today.getSeconds();
  h = checkClock(h);
  m = checkClock(m);
  s = checkClock(s);

  document.querySelector(".clock").innerHTML =
    "Czas serwera: " + h + ":" + m + ":" + s;
  setTimeout(clock, 1000);
};

//////////////////////////////////////////////////////////////////////////////////////////////

document.querySelector(".nav-toggle").addEventListener("click", () => {
  document.querySelector(".nav-links").classList.toggle("active");
});
document.querySelector(".path-name").innerHTML = document.title;