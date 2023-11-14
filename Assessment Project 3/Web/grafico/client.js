let myChart;
let myOtherChart;
let myRealTimeChart;
const socket = new WebSocket('wss://nl2kp0gzc1.execute-api.us-east-1.amazonaws.com/production/');

document.addEventListener('DOMContentLoaded', function () {
    fetchDataAndCreateChart();
    setupDatePickers(); // Agrega la inicialización del calendario
    createRealTimeChart(); // Agregar esta llamada para inicializar la nueva gráfica en tiempo real
  });

socket.addEventListener('message', function (event) {
  const newData = JSON.parse(event.data);
  updateRealTimeChart(newData);
});

socket.addEventListener('error', function (event) {
  console.error('Error en la conexión WebSocket:', event);
});

window.addEventListener('beforeunload', function () {
  socket.close();
});

function setupDatePickers() {
  flatpickr("#startDate", {
    enableTime: true,
    dateFormat: "Y-m-d H:i",
  });
  flatpickr("#endDate", {
    enableTime: true,
    dateFormat: "Y-m-d H:i",
  });
}  

function fetchDataAndCreateChart() {
  fetch('https://mdyyfxmmj1.execute-api.us-east-1.amazonaws.com/Alpha/data')
    .then(response => response.json())
    .then(data => {
      const formattedData = data.map(item => ({
        ...item,
        formattedDate: moment(item.timestamp).format('DD/MM/YYYY HH:mm')
      }));

      const dates = formattedData.map(item => item.formattedDate);
      const values = formattedData.map(item => item.sensor);

      const ctx = document.getElementById('myChart').getContext('2d');
      myChart = new Chart(ctx, {
        type: 'line',
        data: {
          labels: dates,
          datasets: [{
            label: 'Datos del sensor',
            data: values,
            borderColor: 'blue',
            borderWidth: 1,
            fill: false
          }]
        },
        options: {
          scales: {
            x: [{
              type: 'linear',
              position: 'bottom'
            }]
          }
        }
      });
    })
    .catch(error => console.error('Error al obtener los datos:', error));
}

function updateChart() {
  fetch('https://mdyyfxmmj1.execute-api.us-east-1.amazonaws.com/Alpha/data')
    .then(response => response.json())
    .then(newData => {
      const formattedData = newData.map(item => ({
        ...item,
        formattedDate: moment(item.timestamp).format('DD/MM/YYYY HH:mm')
      }));

      const dates = formattedData.map(item => item.formattedDate);
      const values = formattedData.map(item => item.sensor);

      myChart.data.labels = dates;
      myChart.data.datasets[0].data = values;
      myChart.update();
    })
    .catch(error => console.error('Error al obtener los datos:', error));
}

function getLastEntry() {
  fetch('https://mdyyfxmmj1.execute-api.us-east-1.amazonaws.com/Alpha/last-entry')
    .then(response => response.json())
    .then(result => {
      document.getElementById('lastEntryResult').innerText = `Última Entrada: ${result.latest_value.sensor}`;
    })
    .catch(error => console.error('Error al obtener la última entrada:', error));
}

function getMax() {
  fetch('https://mdyyfxmmj1.execute-api.us-east-1.amazonaws.com/Alpha/max')
    .then(response => response.json())
    .then(result => {
      document.getElementById('maxResult').innerText = `Máximo: ${result.max_value}`;
    })
    .catch(error => console.error('Error al obtener el máximo:', error));
}

function getMin() {
  fetch('https://mdyyfxmmj1.execute-api.us-east-1.amazonaws.com/Alpha/min')
    .then(response => response.json())
    .then(result => {
      document.getElementById('minResult').innerText = `Mínimo: ${result.min_value}`;
    })
    .catch(error => console.error('Error al obtener el mínimo:', error));
}

function getAverage() {
  fetch('https://mdyyfxmmj1.execute-api.us-east-1.amazonaws.com/Alpha/average')
    .then(response => response.json())
    .then(result => {
      const averageValue = result.average_value.toFixed(4); // Limitar a 4 decimales
      document.getElementById('averageResult').innerText = `Promedio: ${averageValue}`;
    })
    .catch(error => console.error('Error al obtener el promedio:', error));
}

function getDataBetweenDates() {
    const startDate = moment(document.getElementById('startDate').value).format("YYYY-MM-DDTHH:mm:ss");
    const endDate = moment(document.getElementById('endDate').value).format("YYYY-MM-DDTHH:mm:ss");
  
    const url = `https://mdyyfxmmj1.execute-api.us-east-1.amazonaws.com/Alpha/data-between-dates?start_date=${startDate}&end_date=${endDate}`;
  
    fetch(url)
      .then(response => response.json())
      .then(data => {
        const formattedData = data.map(item => ({
          ...item,
          formattedDate: moment(item.timestamp).format('DD/MM/YYYY HH:mm')
        }));
  
        const dates = formattedData.map(item => item.formattedDate);
        const values = formattedData.map(item => item.sensor);
  
        // Crear el gráfico utilizando Chart.js
        const ctx = document.getElementById('myOtherChart').getContext('2d');
        myOtherChart = new Chart(ctx, {
          type: 'line',
          data: {
            labels: dates,
            datasets: [{
              label: 'Datos del sensor',
              data: values,
              borderColor: 'red', // Puedes cambiar el color según tus preferencias
              borderWidth: 1,
              fill: false
            }]
          },
          options: {
            scales: {
              x: [{
                type: 'linear',
                position: 'bottom'
              }]
            }
          }
        });
      })
      .catch(error => console.error('Error al obtener los datos entre fechas:', error));
  }

  function getDataBetweenHours() {
    const selectedDate = moment(document.getElementById('selectedDate').value).format("YYYY-MM-DD");
    const startTime = moment(document.getElementById('startTime').value, "HH:mm").format("HH:mm:ss");
    const endTime = moment(document.getElementById('endTime').value, "HH:mm").format("HH:mm:ss");
  
    const startDateTime = `${selectedDate}T${startTime}`;
    const endDateTime = `${selectedDate}T${endTime}`;
  
    const url = `https://mdyyfxmmj1.execute-api.us-east-1.amazonaws.com/Alpha/data-between-dates?start_date=${startDateTime}&end_date=${endDateTime}`;
  
    fetch(url)
      .then(response => response.json())
      .then(data => {
        const formattedData = data.map(item => ({
          ...item,
          formattedDate: moment(item.timestamp).format('DD/MM/YYYY HH:mm:ss')
        }));
  
        const dates = formattedData.map(item => item.formattedDate);
        const values = formattedData.map(item => item.sensor);
  
        // Crear el gráfico utilizando Chart.js
        const ctx = document.getElementById('myThirdChart').getContext('2d');
        myThirdChart = new Chart(ctx, {
          type: 'line',
          data: {
            labels: dates,
            datasets: [{
              label: 'Datos del sensor',
              data: values,
              borderColor: 'green', // Puedes cambiar el color según tus preferencias
              borderWidth: 1,
              fill: false
            }]
          },
          options: {
            scales: {
              x: [{
                type: 'linear',
                position: 'bottom'
              }]
            }
          }
        });
      })
      .catch(error => console.error('Error al obtener los datos entre horas:', error));
  }
  

  function updateRealTimeChart(newData) {
    const formattedDate = moment().format('DD/MM/YYYY HH:mm:ss');
  
    // Asumiendo que myRealTimeChart es tu instancia de Chart.js para la nueva gráfica en tiempo real
    myRealTimeChart.data.labels.push(formattedDate);
    myRealTimeChart.data.datasets[0].data.push(newData.sensor);
    
    // Limitar la cantidad de datos mostrados para evitar sobrecargar la gráfica
    const maxDataPoints = 20;
    if (myRealTimeChart.data.labels.length > maxDataPoints) {
      myRealTimeChart.data.labels.shift();
      myRealTimeChart.data.datasets[0].data.shift();
    }
  
    // Actualizar la gráfica
    myRealTimeChart.update();
  }
  
// Función para crear la nueva gráfica en tiempo real
function createRealTimeChart() {
  const ctx = document.getElementById('myRealTimeChart').getContext('2d');
  myRealTimeChart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: [],
      datasets: [{
        label: 'Datos en tiempo real',
        data: [],
        borderColor: 'orange',
        borderWidth: 1,
        fill: false
      }]
    },
    options: {
      scales: {
        x: [{
          type: 'linear',
          position: 'bottom'
        }]
      }
    }
  });
}