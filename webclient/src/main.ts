import {Map as MapLibreMap} from 'maplibre-gl';
import imgUrl from './plan.png'
import Panzoom from '@panzoom/panzoom'

import {ImageControls} from "./ImageControls.ts";
import {ContextMenu} from "./ContextMenu.ts";

import {MapController} from "./controller/MapController.ts";
import {ImageController} from "./controller/ImageController.ts";

import 'maplibre-gl/dist/maplibre-gl.css';
import './style.css';

window.customElements.define('image-controls', ImageControls);

const imgImage: HTMLImageElement = document.getElementById('imgImage')! as HTMLImageElement;
const imageBox: HTMLDivElement = document.getElementById('imageBox')! as HTMLDivElement;
const imgHalf: HTMLDivElement = document.getElementById('imgHalf')! as HTMLDivElement;


const map = new MapLibreMap({
    container: 'map',                                           // HTML element ID where the map will be rendered
    style: 'http://127.0.0.1:8080/styles/osm-liberty/style.json', // Base map style URL
    center: [7.1532, 50.7427],                                      // Initial center of the map
    zoom: 15,                                         // Initial zoom level
});

new MapController(map); // Initialize the MapController with the map instance
new ImageController(imageBox);

new ContextMenu(map, imgImage);

if (imgImage) {
    imgImage.src = imgUrl; // Set the source of the image element to the imported image URL
}

if (imageBox && imgHalf) {
    const panzoom = Panzoom(imageBox, {
        maxScale: 10,
        minScale: 0.1
    });

    let controls = new ImageControls(panzoom, {
        top: '10px',
        right: '10px'
    });

    imgHalf.appendChild(controls);
}