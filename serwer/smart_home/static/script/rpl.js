async function select_rpl(e) {
  switch (e.target.id) {
    case "lamp":
      const dict = { action: "get", id: e.target.value };
      data = await sendData("POST", dict);

      document.querySelectorAll("#rfid").forEach((r) => {
        r.checked = false;
        for (id of data["rfid"]) {
          if (r.value == id) {
            r.checked = true;
            break;
          }
        }
      });
      document.querySelectorAll("#btn").forEach((r) => {
        r.checked = false;
        for (id of data["btn"]) {
          if (r.value == id) {
            r.checked = true;
            break;
          }
        }
      });
      document.querySelector(".mess").innerHTML = "";
      break;
    case "rpl-btn":
      const lamps = document.querySelectorAll("#lamp");
      for (lamp of lamps) {
        if (lamp.checked) {
          rpl_connect();
          document.querySelector(".mess").innerHTML = "Połączono";
          break;
        } else {
          document.querySelector(".mess").innerHTML = "Wybierz lampy";
        }
      }
      break;
  }
}

async function rpl_connect() {
  let lamp = document.querySelectorAll("#lamp");
  let rfid = document.querySelectorAll("#rfid");
  let btn = document.querySelectorAll("#btn");
  let rfids = [];
  let btns = [];
  let lampID;
  lamp.forEach((lamp) => {
    if (lamp.checked) {
      lampID = lamp.value;
    }
  });
  rfid.forEach((rfid) => {
    if (rfid.checked) {
      rfids.push(rfid.value);
    }
  });
  btn.forEach((btn) => {
    if (btn.checked) {
      btns.push(btn.value);
    }
  });
  dict = {
    action: "connect",
    lamp: lampID,
    rfids: rfids,
    btns: btns,
  };

  sendData("POST", dict);
}

window.onload = function () {
  document
    .querySelector(".container")
    .addEventListener("click", select_rpl);
};
