export interface ICoordinate {
    latitude: number;
    longitude: number;
}

export interface IImgCoordinate {
    x: number;
    y: number;
}

export interface ICoordinatePair {
    map: ICoordinate;
    img: IImgCoordinate;
}

export interface IProject {
    id: string;
    name: string;
    description: string;
    min_zoom: number;
    max_zoom: number;
    coordinates: ICoordinatePair[];
    img_scale: { width: number; height: number };
}

export class Project {
    id: string;
    name: string;
    description: string;
    min_zoom: number;
    max_zoom: number;
    coordinates: ICoordinatePair[];
    img_scale: { width: number; height: number };

    constructor(data: IProject) {
        this.id = data.id;
        this.name = data.name;
        this.description = data.description;
        this.min_zoom = data.min_zoom;
        this.max_zoom = data.max_zoom;
        this.coordinates = data.coordinates;
        this.img_scale = data.img_scale;
    }

    public static of(data: IProject): Project {
        return new Project(data);
    }

    public toIProject(): IProject {
        return {
            id: this.id,
            name: this.name,
            description: this.description,
            min_zoom: this.min_zoom,
            max_zoom: this.max_zoom,
            coordinates: this.coordinates,
            img_scale: this.img_scale,
        };
    }
}
