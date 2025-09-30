// ImageControls.ts
// Custom HTML element for providing zoom controls for an image using Panzoom.

import type {PanzoomObject} from "@panzoom/panzoom";

/**
 * Options for positioning the image controls.
 */
type ImageControlOptions = {
    top: string;
    right: string;
}

/**
 * ImageControls is a custom HTML element that provides zoom in/out buttons for an image.
 */
export class ImageControls extends HTMLElement {
    // Panzoom instance for controlling zoom
    private panzoom: PanzoomObject;

    /**
     * Constructs the image controls and attaches zoom buttons.
     * @param panzoom Panzoom instance
     * @param options Positioning options
     */
    constructor(panzoom: PanzoomObject, options: ImageControlOptions ) {
        super();

        this.style.position = 'absolute'
        this.style.top = options.top
        this.style.right = options.right

        this.panzoom = panzoom;
        let imgZoomIN = document.createElement('button');
        imgZoomIN.textContent = "Zoom In";
        imgZoomIN.onclick = () => {
            this.zoomIn();
        };
        this.appendChild(imgZoomIN);
        let imgZoomOut = document.createElement('button');
        imgZoomOut.textContent = "Zoom Out";
        imgZoomOut.onclick = () => {
            this.zoomOut();
        };
        this.appendChild(imgZoomOut);
    }

    /**
     * Zooms in the image.
     */
    zoomIn() {
        this.panzoom.zoomIn();
    }

    /**
     * Zooms out the image.
     */
    zoomOut() {
        this.panzoom.zoomOut();
    }

}