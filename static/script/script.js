function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    var cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      let cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

async function sendData(method, dict,path) {
  const csrftoken = getCookie("csrftoken");
  let data = await fetch(path, {
    method: method,
    headers: { "Content-Type": "application/json", "X-CSRFToken": csrftoken },
    body: JSON.stringify(dict),
  });
  return  data
}

//////////////////////////////////////////////////////////////////////////////////////////////
const waitForElement = (selector, callback) => {
  let interval = setInterval(function () {
    if (document.querySelector(selector)) {
      callback();
      clearInterval(interval);
    }
  }, 50);
};

waitForElement("#nav-toggle", function () {
  document.querySelector("#nav-toggle").addEventListener("click", () => {
    document
      .querySelector("#nav-links")
      .classList.toggle("Navbar__nav-links--active");
  });
});
waitForElement("#path-name", function () {
  document.querySelector("#path-name").innerHTML = document.title;
});
