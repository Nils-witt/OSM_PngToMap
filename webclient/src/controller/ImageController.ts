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

    async showImageOpen() {
        const imgImage: HTMLImageElement = document.getElementById('imgImage')! as HTMLImageElement;
        let btn = document.createElement('button');
        btn.textContent = 'Open Image';
        btn.style.position = 'absolute';
        btn.classList.add('absolute', 'z-2000', 'top-0', 'left-0', 'bg-white', 'h-full', 'w-full', 'text-2xl', 'text-center');
        document.body.appendChild(btn);

        btn.onclick = async () => {
            const [fileHandle] = await window.showOpenFilePicker();
            const file = await fileHandle.getFile();
            imgImage.src = URL.createObjectURL(file)
            btn.remove();
        }

    }
}