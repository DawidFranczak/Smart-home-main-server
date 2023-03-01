const changeLight = async (e) => {
  const lamp = e.target;

  if (lamp.type === "image") {
    dict = {
      action: "change",
      id: lamp.id,
    };

    const dataRep = await sendData("POST", dict);
    console.log(dataRep);
    switch (dataRep["response"]) {
      case "ON":
        lamp.src = "/static/images/lamp_on.png";
        break;
      case "OFF":
        lamp.src = "/static/images/lamp_off.png";
        break;
      default:
        lamp.nextElementSibling.innerHTML = dataRep["response"];
        break;
    }
  }
};

document.querySelector("#led-container").addEventListener("click", changeLight);
