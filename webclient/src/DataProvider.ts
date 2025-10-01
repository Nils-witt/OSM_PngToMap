// DataProvider.ts
// Singleton class for managing and synchronizing image and map coordinates, with event listener support.

import {LngLat} from "maplibre-gl";

/**
 * DataProvider is a singleton for storing and synchronizing coordinates between image and map.
 * It supports event listeners for reactive updates.
 */
export class DataProvider {
    // Singleton instance
    private static instance: DataProvider | null = null;
    // Event listeners mapped by event type
    private listeners: Map<string, ((data: any) => void)[]> = new Map();
    // Stores image coordinates by id
    private imgCoords: Map<number, [number, number]> = new Map();
    // Stores map coordinates by id
    private mapCoords: Map<number, LngLat> = new Map();

    private projectId: string | null = null;

    // Private constructor for singleton
    private constructor() {
        // No initialization required
    }

    /**
     * Returns the singleton instance of DataProvider.
     */
    public static getInstance(): DataProvider {
        if (!DataProvider.instance) {
            DataProvider.instance = new DataProvider();
        }
        return DataProvider.instance;
    }

    /**
     * Adds an event listener for a specific event type.
     * @param eventType Event name
     * @param listener Callback function
     */
    public addListener(eventType: string, listener: ((data: any) => void)): void {
        if (!this.listeners.has(eventType)) {
            this.listeners.set(eventType, []);
        }
        this.listeners.get(eventType)?.push(listener);
    }

    /**
     * Notifies all listeners for a given event.
     * @param event Event name
     * @param data Data to pass to listeners
     */
    private notifyListeners(event: string, data: any): void {
        console.log(`Notifying listeners for event: ${event}`, data);
        if (this.listeners.has(event)) {
            this.listeners.get(event)?.forEach(listener => listener(data));
        }
    }

    /**
     * Sets map coordinates for a given id and notifies listeners.
     * @param id Marker id
     * @param coords Map coordinates (LngLat)
     */
    public setMapCoords(id: number, coords: LngLat): void {
        this.mapCoords.set(id, coords);
        this.notifyListeners('mapCoordsUpdated', {id, coords});
        this.notifyListeners(`mapCoordsUpdated-${id}`, {id, coords});
    }
    /**
     * Gets map coordinates for a given id.
     * @param id Marker id
     */
    public getMapCoords(id: number): LngLat | undefined {
        return this.mapCoords.get(id);
    }
    /**
     * Returns a copy of all map coordinates.
     */
    public getAllMapCoords(): Map<number, LngLat> {
        return new Map(this.mapCoords);
    }

    /**
     * Sets image coordinates for a given id and notifies listeners.
     * @param id Marker id
     * @param coords Image coordinates ([x, y])
     */
    public setImgCoords(id: number, coords: [number, number]): void {
        this.imgCoords.set(id, coords);
        this.notifyListeners('imgCoordsUpdated', {id, coords});
        this.notifyListeners(`imgCoordsUpdated-${id}`, {id, coords});
    }

    /**
     * Gets image coordinates for a given id.
     * @param id Marker id
     */
    public getImgCoords(id: number): [number, number] | undefined {
        return this.imgCoords.get(id);
    }
    /**
     * Returns a copy of all image coordinates.
     */
    public getAllImgCoords(): Map<number, [number, number]> {
        return new Map(this.imgCoords);
    }

    /**
     * Fires a custom event to all listeners for the event name.
     * @param event Event name
     * @param data Data to pass to listeners
     */
    public fireEvent(event: string, data: any): void {
        if (this.listeners.has(event)) {
            this.listeners.get(event)?.forEach(listener => listener(data));
        } else {
            console.warn(`No listeners for event: ${event}`);
        }
    }

    public setProjectId(id: string) {
        this.projectId = id;
    }
    
    public getProjectId(): string | null {
        return this.projectId;
    }
}