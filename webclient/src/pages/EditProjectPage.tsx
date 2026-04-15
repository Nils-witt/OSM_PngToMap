import { useEffect, useRef, useState } from "react";
import { LngLat, Map as MapLibreMap } from "maplibre-gl";
import "../style.scss";
import { TransformComponent, TransformWrapper } from "react-zoom-pan-pinch";
import "maplibre-gl/dist/maplibre-gl.css";
import { DataProvider } from "../data/DataProvider";
import { ApiConnector, type MarkerCoords } from "../data/ApiConnector";
import { MapContextMenu } from "../contextmenu/MapContextMenu";
import { MapController } from "../controller/MapController";
import { ImageController } from "../controller/ImageController";
import { ImageContextMenu } from "../contextmenu/ImageContextMenu";
import { useParams } from "react-router-dom";

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
        y: img_data[1],
      },
      map: {
        latitude: map_data.lat,
        longitude: map_data.lng,
      },
      img_scale: {
        width: imgBox.clientWidth,
        height: imgBox.clientHeight,
      },
    };
    m_data.push(data);
  }

  ApiConnector.setMarkerPositions(
    m_data,
    DataProvider.getInstance().getProjectId()!,
  );
}

export default function EditProjectPage() {
  // create ref for the map div
  const mapRef = useRef<HTMLDivElement | null>(null);
  const imgRef = useRef<HTMLImageElement | null>(null);
  const params = useParams();

  useEffect(() => {}, []);

  useEffect(() => {
    if (params.id) {
      DataProvider.getInstance().setProjectId(params.id);
      ApiConnector.getProjectDetails(params.id).then((data) => {
        let id = 1;
        data.coordinates.forEach((coord: any) => {
          if (coord.img.x !== 0 && coord.img.y !== 0) {
            DataProvider.getInstance().setImgCoords(id, [
              coord.img.x,
              coord.img.y,
            ]);
          }
          if (coord.map.latitude !== 0 && coord.map.longitude !== 0) {
            DataProvider.getInstance().setMapCoords(
              id,
              new LngLat(coord.map.longitude, coord.map.latitude),
            );
          }
          id += 1;
        });
      });
    }
  }, [params.id]);

  useEffect(() => {
    if (mapRef.current) {
      if (!mapRef.current.className.includes("maplibregl-map")) {
        const map = new MapLibreMap({
          container: "map",
          style:
            "https://mapservices.bereitschaften-drk-bonn.de/vector/styles/maptiler-basic/style.json",
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
                <img
                  id="imgImage"
                  alt=""
                  src={ApiConnector.getProjectImageURL(params.id || "")}
                />
              </div>
            </TransformComponent>
          </TransformWrapper>
        </div>
      </div>
      <button
        className={"saveButton"}
        onClick={() => saveDataToApi(imgRef.current)}
      >
        Save
      </button>
    </>
  );
}
