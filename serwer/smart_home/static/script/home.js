const checkClock = (t) => {
    if (t < 10) t = "0" + t;
    return t;
  };
  
  const clock = () => {
    const today = new Date();
    let hours = today.getHours();
    let minutes = today.getMinutes();
    let seconds = today.getSeconds();
    hours = checkClock(hours);
    minutes = checkClock(minutes);
    seconds = checkClock(seconds);
  
    document.querySelector("#clock").innerHTML = `${hours}:${minutes}:${seconds}`;
    setTimeout(clock, 1000);
  };
  
  const date = () =>{
    const today = new Date();
    const day = today.getDate();
    const month = today.getMonth();
    const year = today.getFullYear();
    document.querySelector("#date").innerHTML = `${day}.${month}.${year}`;
  }
  
  const weather = () =>{
    const success = async (position) => {
      const today = new Date();
      const latitude = position.coords.latitude;
      const longitude = position.coords.longitude;
      let place =  await fetch(`https://api.bigdatacloud.net/data/reverse-geocode-client?latitude=${latitude}&longitude=${longitude}&localityLanguage=en`);
      let settings = await fetch(`https://api.open-meteo.com/v1/forecast?latitude=${latitude}&longitude=${longitude}&hourly=temperature_2m`);
      
      settings = await settings.json();
      place = await place.json();

      const temperature = settings.hourly.temperature_2m[today.getHours()];

      document.querySelector("#locality").innerHTML = place.locality;
      document.querySelector("#temp").innerHTML = temperature + "&#8451;";
    }
    const error = () =>{
      document.querySelector("#weather").innerHTML = "...";
    }
    navigator.geolocation.getCurrentPosition(success,error);
    setTimeout(weather, 360000);
  }
  
  clock();
  weather();
  date();