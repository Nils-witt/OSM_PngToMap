
var map = L.map('map').setView([50.703546, 7.127326], 14);
map.setMaxZoom(20);
map.setMinZoom(10);

L.tileLayer('https://map.nilswitt.dev/map/basemap/{z}/{x}/{y}.png').addTo(map);
L.tileLayer('/{z}/{x}/{y}.png').addTo(map);