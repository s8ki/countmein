/* globals Chart:false, feather:false */

  
feather.replace()

// Graphs
var ctx = document.getElementById('myChart')
// eslint-disable-next-line no-unused-vars
var myChart = new Chart(ctx, {
  type: 'line',
  data: {
    labels: [
      'Sunday',
      'Monday',
      'Tuesday',
      'Wednesday',
      'Thursday',
      'Friday',
      'Saturday'
    ],
    datasets: [{
      data: [
        15339,
        21345,
        18483,
        24003,
        23489,
        24092,
        12034
      ],
      lineTension: 0,
      backgroundColor: 'transparent',
      borderColor: '#007bff',
      borderWidth: 4,
      pointBackgroundColor: '#007bff'
    }]
  },
  options: {
    scales: {
      yAxes: [{
        ticks: {
          beginAtZero: false
        }
      }]
    },
    legend: {
      display: false
    }
  }
})

var Piectx = document.getElementById('PieChart')
var PieChart = new Chart(Piectx, {
  type: 'pie',
  data: {
    datasets: [{
      data: [],
      backgroundColor: ['red', 'green'],
    }],
    labels: [
      'Inside',
      'Available',
    ],
  },
  options: {}
});


// REST API
function getStoreData()
{
  //figure out how to get store id in a smart way
  $.getJSON( "/api/store/" + 1, function( data ) {
    var store = data;
    var records_lst = [];
    // updata data about store
    updateEntranceRecords(store, store.entrances[0].id, records_lst);
    setInterval(function(){ 
      updateEntranceRecords(store, store.entrances[0].id, records_lst)
      }, 1000);
  });
}

function updateEntranceRecords(store, entrace_id, records_lst)
{
  //figure out how to get store id in a smart way
  $.getJSON( "/api/store/" + store.id + '/' + entrace_id + '/records/1',
    function(data) {
      var records = data;
      var latest = records[0];

      // update chart
      PieChart.data.datasets.forEach((dataset) => {
        dataset.data.pop();
      });
      var available = latest.inside < store.capacity ? store.capacity - latest.inside : 0;
      PieChart.data.datasets[0].data = [latest.inside, available];
      PieChart.update(0);
      $("#capacity")[0].innerText = store.capacity;
      $("#available")[0].innerText = available;
      $("#inside")[0].innerText = latest.inside;
  });
}

getStoreData();

