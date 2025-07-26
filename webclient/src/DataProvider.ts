import {LngLat} from "maplibre-gl";


export class DataProvider {

    private static instance: DataProvider | null = null;


    private listeners: Map<string, ((data: any) => void)[]> = new Map();


    private imgCoords: Map<number, [number, number]> = new Map();
    private mapCoords: Map<number, LngLat> = new Map();

    private constructor() {

    }

    public static getInstance(): DataProvider {
        if (!DataProvider.instance) {
            DataProvider.instance = new DataProvider();
        }
        return DataProvider.instance;
    }

    public addListener(eventType: string, listener: ((data: any) => void)): void {
        if (!this.listeners.has(eventType)) {
            this.listeners.set(eventType, []);
        }
        this.listeners.get(eventType)?.push(listener);
    }

    private notifyListeners(event: string, data: any): void {
        console.log(`Notifying listeners for event: ${event}`, data);
        if (this.listeners.has(event)) {
            this.listeners.get(event)?.forEach(listener => listener(data));
        }
    }

    public setMapCoords(id: number, coords: LngLat): void {
        this.mapCoords.set(id, coords);
        this.notifyListeners('mapCoordsUpdated', {id, coords});
        this.notifyListeners(`mapCoordsUpdated-${id}`, {id, coords});
    }
    public getMapCoords(id: number): LngLat | undefined {
        return this.mapCoords.get(id);
    }
    public getAllMapCoords(): Map<number, LngLat> {
        return new Map(this.mapCoords);
    }

    public setImgCoords(id: number, coords: [number, number]): void {
        this.imgCoords.set(id, coords);
        this.notifyListeners('imgCoordsUpdated', {id, coords});
        this.notifyListeners(`imgCoordsUpdated-${id}`, {id, coords});
    }

    public getImgCoords(id: number): [number, number] | undefined {
        return this.imgCoords.get(id);
    }
    public getAllImgCoords(): Map<number, [number, number]> {
        return new Map(this.imgCoords);
    }

    public fireEvent(event: string, data: any): void {
        if (this.listeners.has(event)) {
            this.listeners.get(event)?.forEach(listener => listener(data));
        } else {
            console.warn(`No listeners for event: ${event}`);
        }
    }
}