export interface ICoordinate{
    latitude: number;
    longitude: number;
}

export interface IImgCoordinate{
    x: number;
    y: number;
}

export interface ICoordinatePair{
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
    status: string;
}
export class Project {
    id: string;
    name: string;
    description: string;
    min_zoom: number;
    max_zoom: number;
    coordinates: ICoordinatePair[];
    status: string;



    constructor(data: IProject) {
        this.id = data.id;
        this.name = data.name;
        this.description = data.description;
        this.min_zoom = data.min_zoom;
        this.max_zoom = data.max_zoom;
        this.coordinates = data.coordinates;
        this.status = data.status;
    }

    public static of(data: IProject): Project {
        return new Project(data);
    }


}