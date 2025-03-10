
var map = L.map('map').setView([50.74360460211811, 7.1543848507554495], 16);
map.setMaxZoom(20);
map.setMinZoom(10);

L.tileLayer('https://map.nilswitt.dev/map/basemap/{z}/{x}/{y}.png').addTo(map);
L.tileLayer('/{z}/{x}/{y}.png',{maxZoom: 20, minZoom: 10}).addTo(map);