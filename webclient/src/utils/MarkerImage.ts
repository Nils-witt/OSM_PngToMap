// MarkerImage.ts
// Utility class for creating and positioning a colored marker icon using FontAwesome.

import {icon} from "@fortawesome/fontawesome-svg-core";
import {faLocationDot} from "@fortawesome/free-solid-svg-icons/faLocationDot";

/**
 * MarkerImage creates a colored marker icon element and allows positioning it on the page.
 */
export class MarkerImage {
    // The marker icon HTML element
    markerIcon: HTMLElement;

    /**
     * Constructs a marker icon with the specified color.
     * @param color The color of the marker (default: 'blue')
     */
    constructor(color: string = 'blue') {
        this.markerIcon = document.createElement('span');
        this.markerIcon.innerHTML = icon(faLocationDot).html[0];
        this.markerIcon.classList.add( 'z-1000');
        this.markerIcon.style.color = color;
        this.markerIcon.style.position = 'absolute';

    }

    /**
     * Sets the position of the marker icon on the page.
     * @param x X coordinate (pixels)
     * @param y Y coordinate (pixels)
     */
    setPosition(x: number, y: number) {
        this.markerIcon.style.top = (y - this.markerIcon.offsetHeight) + 'px';
        this.markerIcon.style.left = (x - this.markerIcon.offsetWidth / 2) + 'px'
        console.log(this.markerIcon.style.top);
        console.log(this.markerIcon.style.left);
    }

}