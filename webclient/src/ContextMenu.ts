import {LngLat, Map as MapLibreMap, MapMouseEvent} from "maplibre-gl";
import {DataProvider} from "./DataProvider.ts";

export class ContextMenu {

    private container: HTMLDivElement = document.createElement('div');

    private mapCoords: LngLat | null = null;
    private imgCoords: [number, number] | null = null;

    constructor(map: MapLibreMap, imgImage: HTMLImageElement) {

        this.container.classList.add('hidden', 'grid', 'absolute', 'bg-white', 'border', 'border-gray-300', 'shadow-lg', 'rounded-md', 'p-2');
        this.container.oncontextmenu = () => {
            return false;
        };

        let marker1Btn = this.setUpMarker(1, 'red');
        let marker2Btn = this.setUpMarker(2, 'green');
        let marker3Btn = this.setUpMarker(3, 'blue');
        let marker4Btn = this.setUpMarker(4, 'orange');

        this.container.appendChild(marker1Btn);
        this.container.appendChild(marker2Btn);
        this.container.appendChild(marker3Btn);
        this.container.appendChild(marker4Btn);

        document.addEventListener('click', () => {
            this.close();
        });

        map.on('contextmenu', (event) => {
            this.openOnMap(event);
        });

        imgImage.addEventListener('contextmenu', (event: MouseEvent) => {
            event.preventDefault();
            this.openOnImage(event);
            return false;
        });

        document.body.appendChild(this.container);
    }

    private setUpMarker(id: number, color: string): HTMLButtonElement {
        const markerBtn = document.createElement('button');

        markerBtn.textContent = "Marker " + color;

        markerBtn.addEventListener('click', () => {
            if (this.mapCoords) {
                DataProvider.getInstance().setMapCoords(id, this.mapCoords);
            } else if (this.imgCoords) {
                DataProvider.getInstance().setImgCoords(id, this.imgCoords);
            }
            this.close();
        });
        return markerBtn;
    }

    public getContainer(): HTMLDivElement {
        return this.container;
    }

    openOnMap(event: MapMouseEvent) {
        this.close();
        this.mapCoords = event.lngLat;

        this.openOnImageCoords(event.originalEvent.clientX, event.originalEvent.clientY);
    }

    openOnImage(event: MouseEvent) {
        this.close();
        this.imgCoords = [event.offsetX, event.offsetY];

        this.openOnImageCoords(event.clientX, event.clientY);
    }

    private openOnImageCoords(x: number, y: number) {
        this.container.style.top = `${y}px`;
        this.container.style.left = `${x}px`;
        this.container.classList.remove('hidden');
    }

    public close() {
        this.mapCoords = null;
        this.imgCoords = null;
        this.container.classList.add('hidden');
    }
}