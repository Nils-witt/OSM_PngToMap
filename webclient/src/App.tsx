import {useEffect, useRef, useState} from "react";
import {LngLat, Map as MapLibreMap} from "maplibre-gl";
import './style.scss'
import {MapController} from "./controller/MapController.ts";
import {ApiConnector, type MarkerCoords} from "./data/ApiConnector.ts";
import {TransformComponent, TransformWrapper} from "react-zoom-pan-pinch";
import {DataProvider} from "./data/DataProvider.ts";
import 'maplibre-gl/dist/maplibre-gl.css';
import {ImageController} from "./controller/ImageController.ts";
import {MapContextMenu} from "./contextmenu/MapContextMenu.ts";
import {ImageContextMenu} from "./contextmenu/ImageContextMenu.ts";


function saveDataToApi(imgBox: HTMLDivElement | null) {
    let m_data: MarkerCoords[] = [];

    if (!imgBox) {
        console.error("Element with ID 'imageBox' not found in the DOM.");
        return; // Exit the function early to prevent further errors
    }

    for (let i = 1; i <= 4; i++) {
        let img_data = DataProvider.getInstance().getAllImgCoords().get(i);
        let map_data = DataProvider.getInstance().getAllMapCoords().get(i);
        if (!img_data && !map_data) {
            continue;
        }
        if (!img_data) {
            img_data = [0, 0];
        }
        if (!map_data) {
            map_data = new LngLat(0, 0);
        }


        let data: MarkerCoords = {
            img: {
                x: img_data[0],
                y: img_data[1]
            },
            map: {
                latitude: map_data.lat,
                longitude: map_data.lng
            },
            img_scale: {
                width: imgBox.clientWidth,
                height: imgBox.clientHeight
            }
        };
        m_data.push(data);

    }

    ApiConnector.setMarkerPositions(m_data, DataProvider.getInstance().getProjectId()!);
}


function App() {
    // create ref for the map div
    const mapRef = useRef<HTMLDivElement | null>(null);
    const imgRef = useRef<HTMLImageElement | null>(null);
    const [projectId, setProjectId] = useState<string | null>(null);


    useEffect(() => {
        const params = new URL(document.location.toString()).searchParams;
        const projId = params.get("project");
        console.log("Project ID from URL:", projId);
        setProjectId(projId);
        DataProvider.getInstance().setProjectId(projId || "");
    }, [])


    useEffect(() => {
        if (projectId) {
            ApiConnector.getProjectDetails(projectId).then(data => {
                let id = 1;
                data.coordinates.forEach((coord: any) => {
                    if (coord.img.x !== 0 && coord.img.y !== 0) {
                        DataProvider.getInstance().setImgCoords(id, [coord.img.x, coord.img.y]);
                    }
                    if (coord.map.latitude !== 0 && coord.map.longitude !== 0) {
                        DataProvider.getInstance().setMapCoords(id, new LngLat(coord.map.longitude, coord.map.latitude));
                    }
                    id += 1;
                });
            });
        }
    }, [projectId]);

    useEffect(() => {
        if (mapRef.current) {
            if (!mapRef.current.className.includes("maplibregl-map")) {
                const map = new MapLibreMap({
                    container: 'map',
                    style: 'https://sgx.geodatenzentrum.de/gdz_basemapde_vektor/styles/bm_web_col.json',
                    center: [7.1532, 50.7427],
                    zoom: 15,
                });
                new MapController(map);
                new MapContextMenu(map);
            }
        }
    }, [mapRef]);

    useEffect(() => {
        if (imgRef.current) {
            new ImageController(imgRef.current)
            new ImageContextMenu(imgRef.current);
        }
    }, [imgRef]);
    return (
        <>
            <div className="split-container">
                <div className="split-half">
                    <div id="map" ref={mapRef}></div>
                </div>
                <div id="imgHalf" className="split-half image-container">
                    <TransformWrapper>
                        <TransformComponent>
                            <div ref={imgRef}>
                                <img id="imgImage" alt=""
                                     src={ApiConnector.getProjectImageURL(projectId || "")}/>
                            </div>
                        </TransformComponent>
                    </TransformWrapper>
                </div>
            </div>
            <button className={'saveButton'} onClick={() => saveDataToApi(imgRef.current)}>Save</button>
        </>
    )
}

export default App
