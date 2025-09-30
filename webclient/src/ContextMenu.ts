// ContextMenu.ts
// Provides a custom context menu for setting marker coordinates on a map or image.

import {LngLat, Map as MapLibreMap, MapMouseEvent} from "maplibre-gl";
import {DataProvider} from "./DataProvider.ts";

/**
 * ContextMenu class handles the display and logic for a custom context menu
 * that allows users to set marker coordinates on either a map or an image.
 */
export class ContextMenu {
    // The container div for the context menu
    private container: HTMLDivElement = document.createElement('div');
    // Stores the last map coordinates selected
    private mapCoords: LngLat | null = null;
    // Stores the last image coordinates selected
    private imgCoords: [number, number] | null = null;

    /**
     * Initializes the context menu and sets up event listeners.
     * @param map The MapLibre map instance
     * @param imgImage The image element to attach context menu events
     */
    constructor(map: MapLibreMap, imgImage: HTMLImageElement) {

        this.container.classList.add('hidden', 'grid', 'absolute', 'bg-white', 'border', 'border-gray-300', 'shadow-lg', 'rounded-md', 'p-2');
        this.container.style.position = 'absolute';
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
        console.log(this.container);
        document.body.appendChild(this.container);
    }

    /**
     * Creates a button for setting a marker of a specific color and id.
     * @param id Marker id
     * @param color Marker color
     * @returns The button element
     */
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

    /**
     * Returns the container div for the context menu.
     */
    public getContainer(): HTMLDivElement {
        return this.container;
    }

    /**
     * Opens the context menu at the map coordinates from a map event.
     * @param event MapMouseEvent from maplibre-gl
     */
    openOnMap(event: MapMouseEvent) {
        this.close();
        this.mapCoords = event.lngLat;
        this.openOnImageCoords(event.originalEvent.clientX, event.originalEvent.clientY);
    }

    /**
     * Opens the context menu at the image coordinates from a mouse event.
     * @param event MouseEvent from the image
     */
    openOnImage(event: MouseEvent) {
        this.close();
        this.imgCoords = [event.offsetX, event.offsetY];

        this.openOnImageCoords(event.clientX, event.clientY);
    }

    /**
     * Opens the context menu at the specified screen coordinates.
     * @param x X coordinate (pixels)
     * @param y Y coordinate (pixels)
     */
    private openOnImageCoords(x: number, y: number) {
        this.container.style.top = `${y}px`;
        this.container.style.left = `${x}px`;
        this.container.classList.remove('hidden');
    }

    /**
     * Closes the context menu and resets stored coordinates.
     */
    public close() {
        this.mapCoords = null;
        this.imgCoords = null;
        this.container.classList.add('hidden');
    }
}