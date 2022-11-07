function avarage_temp(
  dataAverageData,
  dataAverageTempNight,
  dataAverageTempDay
) {
  for (i in dataAverageData) {

    const il = document.createElement("li");
    const pData = document.createElement("p");
    const pNight = document.createElement("p");
    const pDay = document.createElement("p");

    pData.innerHTML = dataAverageData[i];
    pNight.innerHTML = dataAverageTempNight[i];
    pDay.innerHTML = dataAverageTempDay[i];

    il.appendChild(pData);
    il.appendChild(pNight);
    il.appendChild(pDay);

    document.getElementById("temp_avarage_containers").appendChild(il);
  }
}

function wykres(daneTemp, daneCzas, place) {
  const ctx = document.getElementById("myChart");
  const myChart = new Chart(ctx, {
    type: "line",
    data: {
      labels: daneCzas, // os x
      datasets: [
        {
          label: "Odczyt temperatury co godznę",
          data: daneTemp, // os y
          backgroundColor: ["rgba(0, 0, 0, 0.2)"],
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
  const ctx = document.getElementById("myChart_srednia_dzien");
  const myChart = new Chart(ctx, {
    type: "line",
    data: {
      labels: daneCzas, // os x
      datasets: [
        {
          label: "Średnia temperatura w dzień",
          data: daneTemp, // os y
          backgroundColor: ["rgba(0, 0, 0, 0.2)"],
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
  const ctx = document.getElementById("myChart_srednia_noc");
  const myChart = new Chart(ctx, {
    type: "line",
    data: {
      labels: daneCzas, // os x
      datasets: [
        {
          label: "Średnia temperatura w nocy",
          data: daneTemp, // os y
          backgroundColor: ["rgba(0, 0, 0, 0.2)"],
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
