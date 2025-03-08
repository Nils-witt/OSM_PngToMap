var saveData = (function () {
    var a = document.createElement("a");
    document.body.appendChild(a);
    a.style = "display: none";
    return function (data, fileName) {
        var json = JSON.stringify(data),
            blob = new Blob([json], {type: "octet/stream"}),
            url = window.URL.createObjectURL(blob);
        a.href = url;
        a.download = fileName;
        a.click();
        window.URL.revokeObjectURL(url);
    };
}());

var data = { x: 42, s: "hello, world", d: new Date() },
    fileName = "my-download.json";



var map = L.map('map').setView([50.703546, 7.127326], 14);
map.setMaxZoom(20);
map.setMinZoom(10);


// Replace with your Baselayer map URL to ensure correct alignment
L.tileLayer('https://map.nilswitt.dev/map/basemap/{z}/{x}/{y}.png')
    .addTo(map);


map.on("click", function (e) {
    console.log(e.latlng.lat, e.latlng.lng);
}, 1);

var markers = {};

for (var i = 0; i < 4; i++) {
    var marker = L.marker([50.703546, 7.127326], {draggable: true, title: "Marker " + (i + 1)}).addTo(map);

    marker.bindPopup("<b>Marker " + (i + 1) + "</b><br>", {autoClose: false}).openPopup();
    markers["marker" + i] = marker;
}

document.getElementById("saveBtn").addEventListener("click", function () {
    var data = {};

    for (var key in markers) {
        data[key] = markers[key].getLatLng();
    }

    saveData(data, "test.json");
});



document.getElementById('overlayPicture').onclick = (e) => {
    console.log(e)
    console.log(e.offsetX, e.offsetY);
}