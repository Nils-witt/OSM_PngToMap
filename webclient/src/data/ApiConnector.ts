import { Project } from "./entities/Project";

export type MarkerCoords = {
    img: {
        x: number,
        y: number
    },
    map: {
        latitude: number,
        longitude: number
    },
    img_scale: {
        width: number,
        height: number
    }
};

export class ApiConnector {


    public static backendURL = "http://localhost:80/api/v1/";


    public static getProjectsURL(): string {
        return this.backendURL + "projects/";
    }

    public static getProjectURL(projectId: number): string {
        return this.backendURL + "projects/" + projectId + "/";
    }

    public static getProjectRenderURL(projectId: number): string {
        return this.backendURL + "projects/" + projectId + "/start_render/";
    }

    public static getProjectImageURL(projectId: string): string {
        return ApiConnector.backendURL + "projects/" + projectId + "/image/";
    }
    public static getProjectTiles(projectId: string): string {
        return ApiConnector.backendURL + "projects/" + projectId + "/tiles/";
    }

    public static getProjects(): Promise<Project[]> {
        return fetch(ApiConnector.getProjectsURL())
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                const projects: Project[] = [];

                for (const project of data.results as Project[]) {
                    projects.push(Project.of(project));
                }
                return projects;
            })
            .catch((error) => {
                console.error('Error fetching projects:', error);
                throw error;
            });
    }


    public static setMarkerPositions(data: MarkerCoords[], projectId: string) {
        fetch(this.backendURL + "projects/" + projectId + "/", {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                'coordinates': data
            }),
        })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                console.log('Success:', data);
            })
            .catch((error) => {
                console.error('Error:', error);
            });
    }

    public static async getProjectDetails(projectId: string) {
        const response = await fetch(this.backendURL + "projects/" + projectId + "/", {
            method: 'PATCH'
        })
        return await response.json();
    }

    public static async updateProject(projectId: string, data: { name: string; description: string; min_zoom: number; max_zoom: number }): Promise<void> {
        const response = await fetch(this.backendURL + "projects/" + projectId + "/", {
            method: 'PATCH',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data),
        });
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
    }

    public static setProjectImage(projectId: string, imageFile: File) {
        const formData = new FormData();
        formData.append('image', imageFile);

        fetch(this.backendURL + "projects/" + projectId + "/image/", {
            method: 'POST',
            body: formData,
        })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                console.log('Success:', data);
            })
            .catch((error) => {
                console.error('Error:', error);
            });
    }

    public static startRender(projectId: string) {
        fetch(this.backendURL + "projects/" + projectId + "/start_render/", {
            method: 'POST',
        })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                console.log('Success:', data);
            })
            .catch((error) => {
                console.error('Error:', error);
            });

    }
}