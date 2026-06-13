import { useEffect, useRef, useState } from 'react';
import { LngLat, Map as MapLibreMap } from 'maplibre-gl';
import '../style.scss';
import { TransformComponent, TransformWrapper } from 'react-zoom-pan-pinch';
import 'maplibre-gl/dist/maplibre-gl.css';
import { DataProvider } from '../data/DataProvider';
import { MapContextMenu } from '../contextmenu/MapContextMenu';
import { MapController } from '../controller/MapController';
import { ImageController } from '../controller/ImageController';
import { ImageContextMenu } from '../contextmenu/ImageContextMenu';
import {
    Box,
    Paper,
    Table,
    TableBody,
    TableCell,
    TableContainer,
    TableHead,
    TableRow,
    Typography,
} from '@mui/material';
import { type ICoordinatePair, Project } from '../data/entities/Project.ts';
import { get, set } from 'idb-keyval';

const MARKER_IDS = [1, 2, 3, 4];
const MARKER_COLORS: Record<number, string> = {
    1: 'red',
    2: 'green',
    3: 'blue',
    4: 'orange',
};

type MarkerPosition = {
    img?: [number, number];
    map?: LngLat;
};

export default function EditProjectPage() {
    // create ref for the map div
    const mapRef = useRef<HTMLDivElement | null>(null);
    const imgRef = useRef<HTMLImageElement | null>(null);

    const [confDirHandle, setConfDirHandle] = useState<FileSystemDirectoryHandle | undefined>(
        undefined,
    );

    const [imgUrl, setImgUrl] = useState<string | undefined>(undefined);

    const [markerPositions, setMarkerPositions] = useState<Map<number, MarkerPosition>>(new Map());

    const openDataDirWindow = async () => {
        const dirHandle = await window.showDirectoryPicker();
        await set('workingDirectory', dirHandle);
        setConfDirHandle(dirHandle);
    };

    useEffect(() => {
        if (confDirHandle) {
            void openDataDir(confDirHandle);
        }
    }, [confDirHandle]);

    const openDataDir = async (dirHandle: FileSystemDirectoryHandle) => {
        for await (const entry of dirHandle.values()) {
            if (entry.kind === 'file' && entry.name == 'config.json') {
                await openConfig(entry);
            }
            if (entry.kind === 'file' && entry.name == 'image.png') {
                await openImg(await entry.getFile());
            }
        }
    };

    const openConfig = async (config: FileSystemHandle) => {
        const file = await config.getFile();
        const contents = await file.text();
        const data = JSON.parse(contents);
        const project = Project.of(data);
        console.log(project);

        project.coordinates.forEach((coord, index) => {
            if (coord.img.x !== 0 && coord.img.y !== 0) {
                DataProvider.getInstance().setImgCoords(index + 1, [coord.img.x, coord.img.y]);
            }
            if (coord.map.latitude !== 0 && coord.map.longitude !== 0) {
                DataProvider.getInstance().setMapCoords(
                    index + 1,
                    new LngLat(coord.map.longitude, coord.map.latitude),
                );
            }
        });
    };

    const openImg = async (file: File) => {
        const url = URL.createObjectURL(file);
        setImgUrl(url);
    };

    const saveConfig = () => {
        let m_data: ICoordinatePair[] = [];

        if (!imgRef.current) {
            console.error("Element with ID 'imageBox' not found in the DOM.");
            return; // Exit the function early to prevent further errors
        }
        if (!confDirHandle) {
            console.log('No configuration directory selected.');
            return;
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

            let data: ICoordinatePair = {
                img: {
                    x: img_data[0],
                    y: img_data[1],
                },
                map: {
                    latitude: map_data.lat,
                    longitude: map_data.lng,
                },
            };
            m_data.push(data);
        }
        let pg = new Project({
            id: '',
            name: 'Test',
            description: 'Test description',
            coordinates: m_data,
            min_zoom: 10,
            max_zoom: 14,
            img_scale: {
                width: imgRef.current.clientWidth,
                height: imgRef.current.clientHeight,
            },
        });

        confDirHandle.getFileHandle('config.json', { create: true }).then((fileHandle) => {
            fileHandle.createWritable().then((writable) => {
                writable.write(JSON.stringify(pg.toIProject())).then(() => {
                    writable.close();
                });
            });
        });
    };

    useEffect(() => {
        get('workingDirectory').then((fileHandleOrUndefined) => {
            if (fileHandleOrUndefined) {
                const dirHandle = fileHandleOrUndefined as FileSystemDirectoryHandle;
                setConfDirHandle(dirHandle);
            }
        });

        const updatePosition = (id: number, update: Partial<MarkerPosition>) => {
            setMarkerPositions((prev) => {
                const next = new Map(prev);
                next.set(id, { ...next.get(id), ...update });
                return next;
            });
        };

        MARKER_IDS.forEach((id) => {
            const existingImg = DataProvider.getInstance().getImgCoords(id);
            const existingMap = DataProvider.getInstance().getMapCoords(id);
            if (existingImg || existingMap) {
                updatePosition(id, { img: existingImg, map: existingMap });
            }

            DataProvider.getInstance().addListener(`imgCoordsUpdated-${id}`, (data) => {
                updatePosition(id, { img: data.coords });
            });
            DataProvider.getInstance().addListener(`mapCoordsUpdated-${id}`, (data) => {
                updatePosition(id, { map: data.coords });
            });
        });
    }, []);

    useEffect(() => {
        if (mapRef.current) {
            if (!mapRef.current.className.includes('maplibregl-map')) {
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
            new ImageController(imgRef.current);
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
                                <img id="imgImage" alt="" src={imgUrl} />
                            </div>
                        </TransformComponent>
                    </TransformWrapper>
                </div>
            </div>
            <div className={'controlButtonBox'}>
                <button onClick={saveConfig}>Save</button>
                <button onClick={openDataDirWindow}>Open</button>
            </div>

            <Paper elevation={3} className="markerPositionsBox">
                <Typography variant="subtitle2" sx={{ p: 1, pb: 0 }}>
                    Marker Positions
                </Typography>
                <TableContainer>
                    <Table size="small">
                        <TableHead>
                            <TableRow>
                                <TableCell>#</TableCell>
                                <TableCell>Image (x, y)</TableCell>
                                <TableCell>Map (lat, lng)</TableCell>
                            </TableRow>
                        </TableHead>
                        <TableBody>
                            {MARKER_IDS.map((id) => {
                                const position = markerPositions.get(id);
                                return (
                                    <TableRow key={id}>
                                        <TableCell>
                                            <Box
                                                sx={{
                                                    width: 12,
                                                    height: 12,
                                                    borderRadius: '50%',
                                                    backgroundColor: MARKER_COLORS[id],
                                                }}
                                            />
                                        </TableCell>
                                        <TableCell>
                                            {position?.img
                                                ? `${position.img[0].toFixed(1)}, ${position.img[1].toFixed(1)}`
                                                : '—'}
                                        </TableCell>
                                        <TableCell>
                                            {position?.map
                                                ? `${position.map.lat.toFixed(6)}, ${position.map.lng.toFixed(6)}`
                                                : '—'}
                                        </TableCell>
                                    </TableRow>
                                );
                            })}
                        </TableBody>
                    </Table>
                </TableContainer>
            </Paper>
        </>
    );
}
