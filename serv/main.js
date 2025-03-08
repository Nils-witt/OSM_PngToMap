var map = L.map('map').setView([50.703546, 7.127326], 14);
map.setMaxZoom(20);
map.setMinZoom(10);


// Replace with your Baselayer map URL to ensure correct alignment
L.tileLayer('https://map.nilswitt.dev/map/basemap/{z}/{x}/{y}.png')
    .addTo(map);


map.on("click", function(e) {
    console.log(e.latlng.lat, e.latlng.lng);
 }, 1);