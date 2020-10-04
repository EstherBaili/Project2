var myMap = L.map("map", {
  center: [-37.840935, 144.946457],
  zoom: 5
});


// Adding a tile layer (the background map image) to our map
// We use the addTo method to add objects to our map
L.tileLayer("https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}", {
  attribution: "© <a href='https://www.mapbox.com/about/maps/'>Mapbox</a> © <a href='http://www.openstreetmap.org/copyright'>OpenStreetMap</a> <strong><a href='https://www.mapbox.com/map-feedback/' target='_blank'>Improve this map</a></strong>",
  tileSize: 512,
  maxZoom: 18,
  zoomOffset: -1,
  id: "mapbox/streets-v11",
  accessToken: API_KEY
}).addTo(myMap);


var link = "data1.json";
//var link = "

d3.json(link, function (newresult) {

  var newarray = newresult.features;
  console.log(newarray)
  var markers = L.markerClusterGroup();
  newarray.forEach(x => {
      Object.entries(x).forEach(([geometry, value]) => {
          var location = x.geometry.coordinates
          markers.addLayer(L.marker([location[1], location[0]])
              .bindPopup("<h3>" + (x.properties.JobTitle) +
                  "</h3><hr><p>" + (x.properties.JobCompany) + "</p>")
              )
      })
  })

  myMap.addLayer(markers);
})