var map = L.map('map').setView([50.703546, 7.127326], 14);
map.setMaxZoom(22);
map.setMinZoom(10);

// Replace with your Baselayer map URL to ensure correct alignment
L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    minZoom: 10,
    maxZoom: 22,
}).addTo(map);
L.tileLayer('/tiles/{z}/{x}/{y}', {
    minZoom: 10,
    maxZoom: 22,
}).addTo(map);
