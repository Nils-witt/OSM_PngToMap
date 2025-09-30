// main.ts
// Entry point for the web client. Initializes the map, image controls, context menu, and controllers.

import {Map as MapLibreMap} from 'maplibre-gl';
import Panzoom from '@panzoom/panzoom'
import {ImageControls} from "./ImageControls.ts";
import {ContextMenu} from "./ContextMenu.ts";
import {MapController} from "./controller/MapController.ts";
import {ImageController} from "./controller/ImageController.ts";
import 'tailwindcss';
import 'maplibre-gl/dist/maplibre-gl.css';
import './style.scss';
import {DownloadController} from "./controller/DownloadController.ts";

// Register the custom element for image controls
window.customElements.define('image-controls', ImageControls);

// Get DOM elements for image and containers
const imgImage: HTMLImageElement = document.getElementById('imgImage')! as HTMLImageElement;
const imageBox: HTMLDivElement = document.getElementById('imageBox')! as HTMLDivElement;
const imgHalf: HTMLDivElement = document.getElementById('imgHalf')! as HTMLDivElement;

// Initialize the map with default center and zoom
const map = new MapLibreMap({
    container: 'map',                                           // HTML element ID where the map will be rendered
    style: 'https://karten.bereitschaften-drk-bonn.de/vector/styles/maptiler-basic/style.json', // Base map style URL
    center: [7.1532, 50.7427],                                      // Initial center of the map
    zoom: 15,                                         // Initial zoom level
});

// Initialize controllers and context menu
new MapController(map); // Initialize the MapController with the map instance
const imageController = new ImageController(imageBox);
new ContextMenu(map, imgImage);
new DownloadController();

// Set up panzoom and image controls if containers exist
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

// Show the image open dialog on load
imageController.showImageOpen();