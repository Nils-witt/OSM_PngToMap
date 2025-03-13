// Section: Api

var config = {
    "markers": {},
    "minZoom": 10,
    "maxZoom": 20,
};

function sendToServer() {
    const myHeaders = new Headers();
    myHeaders.append("Content-Type", "application/json");

    const raw = JSON.stringify(config);

    const requestOptions = {
        method: "POST",
        headers: myHeaders,
        body: raw,
        redirect: "follow"
    };
    fetch("/config", requestOptions).then(response => response.text()).then(text => console.log(text));
}

function loadMarkers() {
    fetch("/config")
        .then((response) => response.json())
        .then((result) => {
            config = result;
            for (let i = 0; i < 4; i++) {
                try {
                    document.getElementById('map-pos-' + i).textContent = config.markers[i].map.lat.toFixed(4) + ", " + config.markers[i].map.lng.toFixed(4);
                    document.getElementById('overlay-pos-' + i).textContent = config.markers[i].overlay.x + ", " + config.markers[i].overlay.y;
                } catch (e) {

                }
            }
            document.getElementById('inputMinZoom').value = config.minZoom;
            document.getElementById('inputMaxZoom').value = config.maxZoom;

        })
        .catch((error) => console.error(error));
}


var map = L.map('map').setView([50.703546, 7.127326], 14);
map.setMaxZoom(20);
map.setMinZoom(10);

// Replace with your Baselayer map URL to ensure correct alignment
L.tileLayer('https://sgx.geodatenzentrum.de/wmts_basemapde/tile/1.0.0/de_basemapde_web_raster_farbe/default/GLOBAL_WEBMERCATOR/{z}/{y}/{x}.png').addTo(map);
L.tileLayer('/tiles/{z}/{x}/{y}').addTo(map);

var mapMaker = L.marker([50.703546, 7.127326], {draggable: true, title: "Marker"});
var overlayMarkerPos = {x: 0, y: 0};
var overlayMarker = document.getElementById('overlayMarker');


function selectMarker(id) {
    let marker = config.markers[id];
    if (marker.map.lat != null && marker.map.lng != null) {
        mapMaker.setLatLng([marker.map.lat, marker.map.lng]);
        map.setView([marker.map.lat, marker.map.lng], 15);
    } else {
        mapMaker.setLatLng(map.getCenter());
    }
    if (marker.overlay.x != null && marker.overlay.y != null) {
        overlayMarkerPos.x = marker.overlay.x;
        overlayMarkerPos.y = marker.overlay.y;
        let container = document.getElementById("imageBox")
        container.scrollTop = overlayMarkerPos.y - (container.clientHeight / 2)
        container.scrollLeft = overlayMarkerPos.x - (container.clientWidth / 2)
    }
    updateOverlayMarker();
    mapMaker.addTo(map);
}

function savePosition(id) {
    config.markers[id].map = {
        lat: mapMaker.getLatLng().lat,
        lng: mapMaker.getLatLng().lng
    };
    config.markers[id].overlay = {
        x: overlayMarkerPos.x,
        y: overlayMarkerPos.y
    };
    document.getElementById('map-pos-' + id).textContent = mapMaker.getLatLng().lat.toFixed(4) + ", " + mapMaker.getLatLng().lng.toFixed(4);
    document.getElementById('overlay-pos-' + id).textContent = overlayMarkerPos.x + ", " + overlayMarkerPos.y;
}

function setUpUI() {
    let table = document.getElementById('makertable');

    for (let i = 0; i < 4; i++) {
        config.markers[i] = {
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
}


function updateOverlayMarker() {
    let container = document.getElementById("imageBox")
    let rect = container.getBoundingClientRect();
    let scrollTop = container.scrollTop;
    let scrollLeft = container.scrollLeft;

    let x = ((overlayMarkerPos.x + rect.left) - scrollLeft) - (overlayMarker.width / 2);
    let y = ((overlayMarkerPos.y + rect.top) - scrollTop) - overlayMarker.height;
    overlayMarker.style.left = x + 'px';
    overlayMarker.style.top = y + 'px';
}

document.getElementById('overlayPicture').onclick = (e) => {
    overlayMarkerPos.x = e.offsetX;
    overlayMarkerPos.y = e.offsetY;
    updateOverlayMarker();
}

document.getElementById("imageBox").addEventListener("scroll", updateOverlayMarker);
document.addEventListener('DOMContentLoaded', () => {
    setUpUI();
    loadMarkers();
    updateOverlayMarker();
});

document.getElementById('saveMarkersBtn').addEventListener('click', sendToServer);