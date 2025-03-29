import json
import logging
import os

import cv2
import numpy as np
from PIL import Image
from PIL.Image import DecompressionBombError

from utils import deg2num, find_x_bounds, find_y_bounds, tile_empty

# Remove if you dont trust the images you are working with
Image.MAX_IMAGE_PIXELS = None


class GenerateTiles:
    coordinates: list[list[float]] = []
    picture_points: list[list[int]] = []

    def __init__(
            self,
            tiles_path: str,
            overlay_img_path: str,
            config_path: str,
            zoom: int,
            logger=None,
            tmp_dir: str = "tmp/"
    ):
        self.map_img_offsets = None
        self.x_max = None
        self.x_min = None
        self.y_max = None
        self.y_min = None
        self.osm_tiles = None
        self.tiles_path = tiles_path
        self.overlay_img_path = overlay_img_path
        self.zoom = zoom
        self.logger = logger
        self.config_path = config_path
        self.tmp_dir = tmp_dir

    def create_reference_points(self):
        with open(self.config_path) as json_data:
            d = json.loads(json_data.read())
            json_data.close()
            markers = d['markers']
            self.coordinates: list[list[float]] = [[markers[f]['map']['lat'], markers[f]['map']['lng']] for f in
                                                   markers]
            for coord in self.coordinates:
                print("loaded coordinate", coord)
            self.picture_points: list[list[int]] = [[markers[f]['overlay']['x'], markers[f]['overlay']['y']] for f in
                                                    markers]
            for point in self.picture_points:
                print("Loaded picture point", point)

    def prepare_coordinates_for_warp(self):
        self.osm_tiles = [deg2num(coord[0], coord[1], self.zoom) for coord in self.coordinates]
        # Compute Tiles
        x_tiles = [int(f[0]) for f in self.osm_tiles]
        y_tiles = [int(f[1]) for f in self.osm_tiles]

        x_tiles.sort()
        y_tiles.sort()

        self.y_min = y_tiles[0]
        self.y_max = y_tiles[-1]
        self.x_min = x_tiles[0]
        self.x_max = x_tiles[-1]

        self.logger.info(f"X-Tile-Bounds[{self.zoom}]: {x_tiles} max: {self.x_max} min: {self.x_min}")
        self.logger.info(f"Y-Tile-Bounds[{self.zoom}]: {y_tiles} max: {self.y_max} min: {self.y_min}")

        for (i, val) in enumerate(self.osm_tiles):
            self.logger.info(
                f"[Marker {i + 1}][{self.zoom}] Overlay [{self.picture_points[i][0]}, {self.picture_points[i][1]}] Map [{(val[0] - self.x_min) * 256}, {(val[1] - self.y_min) * 256}]")

        self.map_img_offsets = [(int((val[0] - self.x_min) * 256), int((val[1] - self.y_min) * 256)) for val in
                                self.osm_tiles]

        self.logger.info(f"Map Image Offsets: {self.map_img_offsets}")

    def calulate_target_size(self, im_src):
        return (
            (self.x_max - self.x_min) * 256 * 2,
            (self.y_max - self.y_min) * 256 * 2
        )

    def warp_image(self):
        if len(self.picture_points) < 4:
            self.logger.info("Not enough points to warp image")
            return
        if len(self.map_img_offsets) < 4:
            self.logger.info("Not enough points to warp image")
            return
        if os.path.exists(f"{self.tmp_dir}/overlay_{self.zoom}.png"):
            self.logger.info("Skipping Warp, already exists")
            return
        pts_src = np.array(self.picture_points)
        pts_dst = np.array(self.map_img_offsets)

        h, status = cv2.findHomography(pts_src, pts_dst)
        im_src = cv2.imread(self.overlay_img_path, cv2.IMREAD_UNCHANGED)
        target_pic_size = self.calulate_target_size(im_src)

        im_out = cv2.warpPerspective(
            im_src,
            h,
            target_pic_size
        )

        cv2.imwrite(f"{self.tmp_dir}/overlay_{self.zoom}.png", im_out)

    def crop_image(self):
        if os.path.exists(f"{self.tmp_dir}/overlay_{self.zoom}_crop.png"):
            self.logger.info("Skipping crop, already exists")
            return
        src_img = Image.open(f"{self.tmp_dir}/overlay_{self.zoom}.png")
        lower_y = find_y_bounds(src_img)
        right_x = find_x_bounds(src_img)
        cropped = src_img.crop((0, 0, right_x, lower_y))
        cropped.save(f"{self.tmp_dir}/overlay_{self.zoom}_crop.png")

    def generate_tiles(self):
        try:
            src_img = Image.open(f"{self.tmp_dir}/overlay_{self.zoom}_crop.png")
            src_height = src_img.height
            src_width = src_img.width
        except DecompressionBombError:
            self.logger.error(f"DecompressionBombError")
            return

        self.logger.info(f"Src Image[{self.zoom}]: {src_width}, {src_height}")
        tile_size = 256

        x_offset = 0

        while x_offset < (src_width / tile_size):
            current_x_dir: str = f"{self.tiles_path}/{self.zoom}/{x_offset + self.x_min}"
            os.makedirs(current_x_dir, exist_ok=True)
            y_offset = 0
            while y_offset < (src_height / tile_size):
                self.logger.info(
                    f"Generating Tile[{self.zoom}]: {x_offset} (of {(src_width / tile_size)}) / {y_offset} (of {(src_height / tile_size)})")
                tile = src_img.crop((x_offset * tile_size,
                                     y_offset * tile_size,
                                     x_offset * tile_size + tile_size,
                                     y_offset * tile_size + tile_size))
                if not tile_empty(tile):
                    tile.save(f"{current_x_dir}/{y_offset + self.y_min}.png")
                y_offset += 1
            if len(os.listdir(current_x_dir)) == 0:
                os.rmdir(current_x_dir)
            x_offset += 1

    def run(self):
        self.logger.info("Starting")
        self.create_reference_points()
        self.prepare_coordinates_for_warp()
        self.warp_image()
        self.crop_image()
        self.generate_tiles()
        self.logger.info("Done")
