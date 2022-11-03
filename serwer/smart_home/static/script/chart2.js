function avarage_temp(
  data_average_data,
  data_average_temp_night,
  data_average_temp_day
) {
  for (i in data_average_data) {
    let il = document.createElement("li");
    let pData = document.createElement("p");
    let pNight = document.createElement("p");
    let pDay = document.createElement("p");
    pData.innerHTML = data_average_data[i];
    pNight.innerHTML = data_average_temp_night[i];
    pDay.innerHTML = data_average_temp_day[i];
    il.appendChild(pData);
    il.appendChild(pNight);
    il.appendChild(pDay);
    document.getElementById("temp_avarage_containers").appendChild(il);
  }
}

function wykres(dane_temp, dane_czas, place) {
  const ctx = document.getElementById("myChart");
  const myChart = new Chart(ctx, {
    type: "line",
    data: {
      labels: dane_czas, // os x
      datasets: [
        {
          label: "Odczyt temperatury co godznę",
          data: dane_temp, // os y
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

function wykres_srednia_dzien(dane_temp, dane_czas, place) {
  const ctx = document.getElementById("myChart_srednia_dzien");
  const myChart = new Chart(ctx, {
    type: "line",
    data: {
      labels: dane_czas, // os x
      datasets: [
        {
          label: "Średnia temperatura w dzień",
          data: dane_temp, // os y
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

function wykres_srednia_noc(dane_temp, dane_czas, place) {
  const ctx = document.getElementById("myChart_srednia_noc");
  const myChart = new Chart(ctx, {
    type: "line",
    data: {
      labels: dane_czas, // os x
      datasets: [
        {
          label: "Średnia temperatura w nocy",
          data: dane_temp, // os y
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
