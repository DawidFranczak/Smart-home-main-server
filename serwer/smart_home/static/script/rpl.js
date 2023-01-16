const rplConnect = async () => {
  const lamp = document.querySelectorAll("#lamp");
  const rfid = document.querySelectorAll("#rfid");
  const btn = document.querySelectorAll("#button");

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

  const dict = {
    action: "connect",
    lamp: lampID,
    rfids: rfids,
    btns: btns,
  };

  const response = await sendData("POST", dict);
  document.querySelector("#mess").innerHTML = response["message"];
};

const rplSelect = async (e) => {
  const target = e.target;
  document.querySelector("#mess").innerHTML = "";
  switch (target.id) {
    case "lamp":
      const dict = {
        action: "get",
        id: target.value,
      };

      const data = await sendData("POST", dict);

      document.querySelectorAll("#rfid").forEach((r) => {
        r.checked = false;
        for (id of data["rfid"]) {
          if (r.value == id) {
            r.checked = true;
            break;
          }
        }
      });

      document.querySelectorAll("#button").forEach((r) => {
        r.checked = false;
        for (id of data["btn"]) {
          if (r.value == id) {
            r.checked = true;
            break;
          }
        }
      });

      document.querySelector("#mess").innerHTML = "";
      break;
    case "rpl-btn":
      const lamps = document.querySelectorAll("#lamp");
      let flag = false;

      for (let lamp of lamps) {
        if (lamp.checked) {
          rplConnect();
          flag = true;
          break;
        }
      }
      if (!flag) document.querySelector("#mess").innerHTML = "Wybierz lampy";
      break;
  }
};

window.onload = function () {
  document.querySelector(".container").addEventListener("click", rplSelect);
};
