const changeLight = async (e) => {
  const lamp = e.target;

  if (lamp.type === "image") {
    dict = {
      action: "change",
      id: lamp.id,
    };

    const dataRep = await sendData("POST", dict);
    switch (dataRep["response"]) {
      case 1:
        lamp.src = "/static/images/lamp_on.png";
        break;
      case 0:
        lamp.src = "/static/images/lamp_off.png";
        break;
      case -1:
        lamp.nextElementSibling.innerHTML = "Nie udało się połączyć z lampą";
        break;
    }
  }
};

document.querySelector("#led-container").addEventListener("click", changeLight);
