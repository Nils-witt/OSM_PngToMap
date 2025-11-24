import {Map as MapLibreMap, Marker, NavigationControl} from 'maplibre-gl';
import {DataProvider} from "../data/DataProvider.ts";


export class MapController {

    private map: MapLibreMap;

    constructor(map: MapLibreMap) {
        this.map = map;
        map.on('load', () => {
            let navControl = new NavigationControl({
                showCompass: true,      // Show compass for rotation
                visualizePitch: true,   // Show pitch control
                showZoom: true          // Show zoom controls
            });
            map.addControl(navControl, 'top-right');

        });
        this.setUpMarkers();
    }

    private setUpMarkers() {
        this.setUpMarker(1, 'red');
        this.setUpMarker(2, 'green');
        this.setUpMarker(3, 'blue');
        this.setUpMarker(4, 'orange');
    }

    private setUpMarker(id: number, color: string) {
        let marker = new Marker({
            color: color,
        });

        DataProvider.getInstance().addListener(`mapCoordsUpdated-${id}`, (data) => {
            marker.setLngLat(data.coords).addTo(this.map);
        });
    }
}