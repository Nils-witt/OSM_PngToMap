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

var map = L.map('map').setView([50.703546, 7.127326], 14);
map.setMaxZoom(20);
map.setMinZoom(10);

// Replace with your Baselayer map URL to ensure correct alignment
L.tileLayer('https://map.nilswitt.dev/map/basemap/{z}/{x}/{y}.png').addTo(map);

map.on("click", function (e) {
    console.log(e.latlng.lat, e.latlng.lng);
}, 1);

var mapMaker = L.marker([50.703546, 7.127326], {draggable: true, title: "Marker"});
var overlayMarkerPos = {x: 0, y: 0};
var markers = {};

function selectMarker(id) {
    let marker = markers[id];
    if (marker.map.lat != null && marker.map.lng != null) {
        mapMaker.setLatLng([marker.map.lat, marker.map.lng]);
    } else {
        mapMaker.setLatLng(map.getCenter());
    }
    mapMaker.addTo(map);
}

function savePosition(id) {
    markers[id].map = {
        lat: mapMaker.getLatLng().lat,
        lng: mapMaker.getLatLng().lng
    }
    markers[id].overlay = {
        x: overlayMarkerPos.x,
        y: overlayMarkerPos.y
    }
    document.getElementById('map-pos-' + id).textContent = mapMaker.getLatLng().lat.toFixed(4) + ", " + mapMaker.getLatLng().lng.toFixed(4);
    document.getElementById('overlay-pos-' + id).textContent = overlayMarkerPos.x + ", " + overlayMarkerPos.y;
}

let table = document.getElementById('makertable');

for (let i = 0; i < 4; i++) {
    markers[i] = {
        map: {
            lat: null,
            lng: null
        },
        overlay: {
            x: null,
            y: null
        }
    };

    let row = document.createElement('tr');
    let name = document.createElement('td');
    name.textContent = "Maker " + (i + 1);
    row.appendChild(name);

    let select = document.createElement('button');
    select.textContent = "Select";
    select.addEventListener('click', () => selectMarker(i));
    row.appendChild(select);

    let save = document.createElement('button');
    save.textContent = "Save";
    save.addEventListener('click', () => savePosition(i));
    row.appendChild(save);
    let overlayPos = document.createElement('td');
    overlayPos.id = "overlay-pos-" + i;
    overlayPos.textContent = "N/A";
    let mapPos = document.createElement('td');
    mapPos.id = "map-pos-" + i;
    mapPos.textContent = "N/A";
    row.appendChild(overlayPos);
    row.appendChild(mapPos);

    table.appendChild(row);
}

document.getElementById("saveBtn").addEventListener("click", function () {
    saveData(markers, "test.json");
});


var overlayMarker = document.getElementById('overlayMarker');


document.getElementById('overlayPicture').onclick = (e) => {
    overlayMarkerPos.x = e.offsetX;
    overlayMarkerPos.y = e.offsetY;
    updateOverlayMarker();
}


document.getElementById("testBtn").addEventListener("click", function (e) {

});

function updateOverlayMarker() {
    let container = document.getElementById("imageBox")
    let rect = container.getBoundingClientRect();
    let scrollTop = container.scrollTop;
    let scrollLeft = container.scrollLeft;

    let x = ((overlayMarkerPos.x + rect.left) - scrollLeft) - (overlayMarker.width / 2);
    let y = ((overlayMarkerPos.y + rect.top) - scrollTop) - overlayMarker.height;
    console.log(x, y);
    overlayMarker.style.left = x + 'px';
    overlayMarker.style.top = y + 'px';
}

document.getElementById("imageBox").addEventListener("scroll", function (e) {
    updateOverlayMarker();
});

document.addEventListener('DOMContentLoaded', function () {
    updateOverlayMarker();
})