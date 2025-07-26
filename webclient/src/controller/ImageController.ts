import {MarkerImage} from "../utils/MarkerImage.ts";
import {DataProvider} from "../DataProvider.ts";


export class ImageController {

    private imageBox: HTMLElement;

    constructor(imageBox: HTMLElement) {
        this.imageBox = imageBox;
        this.setUpMarkers();
    }

    private setUpMarkers() {
        this.setUpMarker(1, 'red');
        this.setUpMarker(2, 'green');
        this.setUpMarker(3, 'blue');
        this.setUpMarker(4, 'orange');
    }

    private setUpMarker(id: number, color: string) {
        let marker = new MarkerImage(color);
        this.imageBox.appendChild(marker.markerIcon);

        DataProvider.getInstance().addListener(`imgCoordsUpdated-${id}`, (data) => {
            marker.setPosition(data.coords[0], data.coords[1]);
        });
    }
}