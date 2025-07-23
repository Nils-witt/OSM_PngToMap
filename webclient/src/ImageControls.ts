import type {PanzoomObject} from "@panzoom/panzoom";


type ImageControlOptions = {
    top: string;
    right: string;
}

export class ImageControls extends HTMLElement {
    private panzoom: PanzoomObject;

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

    zoomIn() {
        this.panzoom.zoomIn();
    }

    zoomOut() {
        this.panzoom.zoomOut();
    }

}