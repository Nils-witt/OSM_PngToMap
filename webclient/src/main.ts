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
import { ApiConnector } from './ApiConnector.ts';
import { DataProvider } from './DataProvider.ts';
import { LngLat } from 'maplibre-gl';

// Register the custom element for image controls
window.customElements.define('image-controls', ImageControls);

let params = new URL(document.location.toString()).searchParams;
const project_id = params.get("project");
console.log(project_id);

DataProvider.getInstance().setProjectId(project_id);
// Get DOM elements for image and containers
const imgImage: HTMLImageElement = document.getElementById('imgImage')! as HTMLImageElement;
const imageBox: HTMLDivElement = document.getElementById('imageBox')! as HTMLDivElement;
const imgHalf: HTMLDivElement = document.getElementById('imgHalf')! as HTMLDivElement;

// Initialize the map with default center and zoom
const map = new MapLibreMap({
    container: 'map',
    style: 'https://sgx.geodatenzentrum.de/gdz_basemapde_vektor/styles/bm_web_col.json',
    center: [7.1532, 50.7427],
    zoom: 15,
});

new MapController(map);
const imageController = new ImageController(imageBox);
imageController.getImage().src = ApiConnector.getProjectImageURL(project_id);
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

ApiConnector.getProjectDetails(project_id).then(data => {
    console.log("Loaded marker positions:", data);
    let id = 1;
    data.coordinates.forEach(coord => {
        console.log("Setting marker:", coord);
        if(coord.img.x !== 0 && coord.img.y !== 0){
            DataProvider.getInstance().setImgCoords(id, [coord.img.x, coord.img.y]);
        }
        if(coord.map.latitude !== 0 && coord.map.longitude !== 0){
            DataProvider.getInstance().setMapCoords(id, new LngLat(coord.map.longitude, coord.map.latitude));
        }
        
        id += 1;
        
    });
    /*
       DataProvider.getInstance().setMapCoords(id, this.mapCoords);
            } else if (this.imgCoords) {
                DataProvider.getInstance().setImgCoords(id, this.imgCoords);
            }
                */
});