
export type MarkerCoords = {
    img:{
        x:number,
         y:number
    },
    map: {
        latitude:number,
         longitude:number
    },
    img_scale: {
        width: number,
        height: number
    }
};

export class ApiConnector {


    public static backendURL = "http://localhost:8000/api/v1/";



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
        return ApiConnector.backendURL + "projects/" + projectId + "/get_image/";
    }



    public static setMarkerPositions(data: MarkerCoords[], projectId: string) {
        console.log("Setting marker positions for project:", projectId);
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
}