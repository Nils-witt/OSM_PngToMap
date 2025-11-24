import type {ContextMenuInterface} from "./ContextMenuInterface.ts";
import {DataProvider} from "../data/DataProvider.ts";

export class ImageContextMenu implements ContextMenuInterface {
    // The container div for the context menu
    private container: HTMLDivElement = document.createElement('div');
    // Stores the last map coordinates selected
    private coordinates: [number, number] | null = null;

    /**
     * Initializes the context menu and sets up event listeners.
     * @param imgImage
     */
    constructor(imgImage: HTMLImageElement) {

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

        imgImage.addEventListener('contextmenu', (event: MouseEvent) => {
            console.log(event);
            event.preventDefault();
            this.openOnImage(event);
            return false;
        });
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
            if (this.coordinates) {
                DataProvider.getInstance().setImgCoords(id, this.coordinates);
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

    open(x: number, y: number) {
        this.openOnScreenCoords(x, y);
    }

    /**
     * Opens the context menu at the image coordinates from a mouse event.
     * @param event MouseEvent from the image
     */
    openOnImage(event: MouseEvent) {
        this.close();
        this.coordinates = [event.offsetX, event.offsetY];

        this.openOnScreenCoords(event.clientX, event.clientY);
    }

    /**
     * Opens the context menu at the specified screen coordinates.
     * @param x X coordinate (pixels)
     * @param y Y coordinate (pixels)
     */
    private openOnScreenCoords(x: number, y: number) {
        this.container.style.top = `${y}px`;
        this.container.style.left = `${x}px`;
        this.container.style.visibility = 'visible';
    }

    /**
     * Closes the context menu and resets stored coordinates.
     */
    public close() {
        this.coordinates = null;
        this.container.style.visibility = 'hidden';
    }
}