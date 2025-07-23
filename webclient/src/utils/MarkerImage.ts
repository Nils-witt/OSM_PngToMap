import {icon} from "@fortawesome/fontawesome-svg-core";
import {faLocationDot} from "@fortawesome/free-solid-svg-icons/faLocationDot";

export class MarkerImage {
    markerIcon: HTMLElement;

    constructor(color: string = 'blue') {
        this.markerIcon = document.createElement('span');
        this.markerIcon.innerHTML = icon(faLocationDot).html[0];
        this.markerIcon.classList.add('absolute', 'z-1000');
        this.markerIcon.style.color = color;

    }

    setPosition(x: number, y: number) {
        this.markerIcon.style.top = (y - this.markerIcon.offsetHeight) + 'px';
        this.markerIcon.style.left = (x - this.markerIcon.offsetWidth / 2) + 'px';
    }

}