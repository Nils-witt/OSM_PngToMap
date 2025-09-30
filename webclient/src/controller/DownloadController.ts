// DownloadController.ts
// Provides a UI button and logic to download the current image and map coordinates as a JSON file.

import {DataProvider} from "../DataProvider.ts";

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
        let data = {
            img: {}, map: {}
        };

        for (const [key, value] of DataProvider.getInstance().getAllImgCoords().entries()) { // Using the default iterator (could be `map.entries()` instead)
            data.img[key] = {
                x: value[0],
                y: value[1]
            };
        }
        for (const [key, value] of DataProvider.getInstance().getAllMapCoords().entries()) { // Using the default iterator (could be `map.entries()` instead)
            data.map[key] = {
                latitude: value.lat,
                longitude: value.lng
            };
        }
        let imgBox = document.getElementById('imageBox');

        data['img_scale'] = {
            width: imgBox.clientWidth,
            height: imgBox.clientHeight
        }
        console.log(JSON.stringify(data));
        let blob = new Blob([JSON.stringify(data)], {type: "application/json"});

        let a = document.createElement('a');
        a.download = "data.json";
        a.href = URL.createObjectURL(blob);
        a.dataset.downloadurl = ["application/json", a.download, a.href].join(':');
        a.style.display = "none";
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        setTimeout(function () {
            URL.revokeObjectURL(a.href);
        }, 1500);
    }
}