// REST API
function getStoreData()
{
  //figure out how to get store id in a smart way
  $.getJSON( "/api/store/" + store_id, function( data ) {
    var store = data;
    // updata data about store
    updateTrafficLight(store, store.entrances[0].id);
    setInterval(function(){ 
      updateTrafficLight(store, store.entrances[0].id)
      }, 500);
  });
}

function updateTrafficLight(store, entrace_id)
{
  //figure out how to get store id in a smart way
  $.getJSON( "/api/store/" + store.id + '/' + entrace_id + '/records/1',
    function(data) {
      var records = data;
      var latest = records[0];


      var available = latest.inside < store.capacity ? store.capacity - latest.inside : 0;
      $("#capacity")[0].innerText = store.capacity;
    //   $("#available")[0].innerText = available;
      $("#inside")[0].innerText = latest.inside;

      var traffic_img = 0 < available ? "traffic_green.png" : "traffic_red.png";
      $("#trafficlight").attr("src","/static/" + traffic_img);
  });
}

getStoreData();