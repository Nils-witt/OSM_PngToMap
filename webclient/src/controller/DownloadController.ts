// DownloadController.ts
// Provides a UI button and logic to download the current image and map coordinates as a JSON file.

import { ApiConnector, MarkerCoords } from "../ApiConnector.ts";
import {DataProvider} from "../DataProvider.ts";
import { LngLat } from "maplibre-gl";
/**
 * DownloadController creates a floating download button and handles exporting
 * the current image and map coordinates, including image scale, to a JSON file.
 */
export class DownloadController {
    // The download button element
    private button: HTMLButtonElement = document.createElement('button');

    /**
     * Initializes the download button and attaches it to the document.
     */
    constructor() {
        this.button.classList.add( "z-1000", "bg-white", "border", "border-gray-300", "shadow-lg", "rounded-md", "p-2", 'hover:cursor-pointer', 'hover:bg-gray-100');
        this.button.innerText = "Download";
        this.button.style.position = "absolute";
        this.button.style.top = "0px";
        this.button.style.left = "0px";

        this.button.onclick = this.downloadConfig;

        document.body.appendChild(this.button);
    }

    /**
     * Gathers all coordinates and image scale, then triggers a JSON file download.
     */
    public downloadConfig() {
        let m_data: MarkerCoords[] = [];
        let imgBox = document.getElementById('imageBox');

        if (!imgBox) {
            console.error("Element with ID 'imageBox' not found in the DOM.");
            return; // Exit the function early to prevent further errors
        }

        for(let i = 1; i <= 4; i++) {
            let img_data = DataProvider.getInstance().getAllImgCoords().get(i);
            let map_data = DataProvider.getInstance().getAllMapCoords().get(i);
            if(!img_data && !map_data){
                continue;
            }
            if(!img_data){
                img_data = [0,0];
            }
            if(!map_data){
                map_data = new LngLat(0,0);
            }


            let data: MarkerCoords = {
                img: {
                    x: img_data[0],
                    y: img_data[1]
                }, 
                map: {
                    latitude: map_data.lat,
                    longitude: map_data.lng
                },
                img_scale: {
                    width: imgBox.clientWidth,
                    height: imgBox.clientHeight
                }
            };
            console.log(data);
            m_data.push(data);

        }

       ApiConnector.setMarkerPositions(m_data, DataProvider.getInstance().getProjectId()!);
    }
}