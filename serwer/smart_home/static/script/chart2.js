function avarage_temp(
  dataAverageData,
  dataAverageTempNight,
  dataAverageTempDay
) {
  for (i in dataAverageData) {

    const li = document.createElement("li");
    const data = document.createElement("p");
    const tempNight = document.createElement("p");
    const tempDay = document.createElement("p");

    data.innerHTML = dataAverageData[i];
    data.setAttribute('class','Temp-avarage__li__p-data');

    tempNight.innerHTML = dataAverageTempNight[i];
    tempNight.setAttribute('class','Temp-avarage__li__p-night');

    tempDay.innerHTML = dataAverageTempDay[i];
    tempDay.setAttribute('class','Temp-avarage__li__p-day');

    li.setAttribute('class','Temp-avarage__li')
    li.appendChild(data);
    li.appendChild(tempDay);
    li.appendChild(tempNight);

    document.querySelector("#temp_avarage_containers").appendChild(li);
  }
}



function wykres(daneTemp, daneCzas, place) {
  const ctx = document.querySelector("#myChart");
  const myChart = new Chart(ctx, {
    type: "line",
    data: {
      labels: daneCzas, // os x
      datasets: [
        {
          label: "Odczyt temperatury co godznę",
          data: daneTemp, // os y
          backgroundColor: ["rgba(0, 0, 0, 0)"],
          borderColor: 'rgb(0,0,0,0.5)',
          pointBorderColor: 'rgba(255, 255, 255,0)'
        },
      ],
    },
    options: {
      plugins: {
        legend: {
          labels: {
            font: {
              size: 16,
            },
          },
        },
        title: {
          display: true,
          text: place,
          font: { size: 20 },
          color: ["#000"],
        },
      },
    },
  });
}

function wykres_srednia_dzien(daneTemp, daneCzas, place) {
  const ctx = document.querySelector("#myChart_average_temp_day");
  const myChart = new Chart(ctx, {
    type: "line",
    data: {
      labels: daneCzas,
      datasets: [
        {
          label: "Średnia temperatura w dzień",
          data: daneTemp,
          backgroundColor: ["rgba(0, 0, 0, 0)"],
          borderColor: 'rgb(0,0,0,0.5)',
          pointBorderColor: 'rgba(255, 255, 255,0)'
        },
      ],
    },
    options: {
      plugins: {
        legend: {
          labels: {
            font: {
              size: 16,
            },
          },
        },
        title: {
          display: true,
          text: place,
          font: { size: 20 },
          color: ["#000"],
        },
      },
    },
  });
}

function wykres_srednia_noc(daneTemp, daneCzas) {
  const ctx = document.querySelector("#myChart_average_temp_night");
  const myChart = new Chart(ctx, {
    type: "line",
    data: {
      labels: daneCzas,
      datasets: [
        {
          label: "Średnia temperatura w nocy",
          data: daneTemp,
          backgroundColor: ["rgba(0, 0, 0, 0)"],
          borderColor: 'rgb(0,0,0,0.5)',
          pointBorderColor: 'rgba(255, 255, 255,0)'
        },
      ],
    },
    options: {
      plugins: {
        legend: {
          labels: {
            font: {
              size: 16,
            },
          },
        },
      },
    },
  });
}
