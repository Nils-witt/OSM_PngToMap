import os

import cv2
import numpy as np
from PIL import Image
from PIL.Image import DecompressionBombError
import json
from utils import deg2num

# Remove if you dont trust the images you are working with
Image.MAX_IMAGE_PIXELS = None


def tile_empty(tile) -> bool:
    for x in range(0, tile.width):
        for y in range(0, tile.height):
            if tile.getpixel((x, y)) != (0, 0, 0, 0):
                return False
    return True


class GenerateTiles:
    coordinates: list[list[float]] = []
    picture_points: list[list[int]] = []

    def __init__(self, tiles_path: str, overlay_img_path: str, zoom: int):
        self.map_img_offsets = None
        self.x_max = None
        self.x_min = None
        self.y_max = None
        self.y_min = None
        self.osm_tiles = None
        self.tiles_path = tiles_path
        self.overlay_img_path = overlay_img_path
        self.zoom = zoom

    def create_reference_points(self):
        with open('input/markers.json') as json_data:
            d = json.loads(json_data.read())
            json_data.close()
            self.coordinates: list[list[float]] = [[d[f]['map']['lat'],d[f]['map']['lng']] for f in d]
            self.picture_points: list[list[int]] = [[d[f]['overlay']['x'],d[f]['overlay']['y']] for f in d]

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

        print(f"X-Tiles[{self.zoom}]: {x_tiles} max: {self.x_max} min: {self.x_min}")
        print(f"Y-Tiles[{self.zoom}]: {y_tiles} max: {self.y_max} min: {self.y_min}")

        for (i, val) in enumerate(self.osm_tiles):
            print(
                f"[Marker {i + 1}][{self.zoom}] Overlay [{self.picture_points[i][0]}, {self.picture_points[i][1]}] Map [{(val[0] - self.x_min) * 256}, {(val[1] - self.y_min) * 256}]")

        self.map_img_offsets = [(int((val[0] - self.x_min) * 256), int((val[1] - self.y_min) * 256)) for val in
                                self.osm_tiles]

        print(f"Map Image Offsets: {self.map_img_offsets}")

    def warp_image(self):
        if len(self.picture_points) < 4:
            print("Not enough points to warp image")
            return
        if len(self.map_img_offsets)  < 4:
            print("Not enough points to warp image")
            return
        pts_src = np.array(self.picture_points)
        pts_dst = np.array(self.map_img_offsets)

        h, status = cv2.findHomography(pts_src, pts_dst)
        im_src = cv2.imread(self.overlay_img_path, cv2.IMREAD_UNCHANGED)
        im_out = cv2.warpPerspective(
            im_src,
            h,
            ((self.x_max - self.x_min) * 265 * 2, (self.y_max - self.y_min) * 265 * 2)
        )
        os.makedirs(f"tmp", exist_ok=True)
        cv2.imwrite(f"tmp/{self.zoom}.png", im_out)

    def generate_tiles(self):
        try:
            src_img = Image.open(f"tmp/{self.zoom}.png")
            src_height = src_img.height
            src_width = src_img.width
        except DecompressionBombError:
            print(f"DecompressionBombError")
            return

        print(f"Src Image[{self.zoom}]: {src_width}, {src_height}")
        tile_size = 256

        x_offset = 0

        while x_offset < (src_width / tile_size):
            os.makedirs(f"{self.tiles_path}/{self.zoom}/{x_offset + self.x_min}", exist_ok=True)
            y_offset = 0
            while y_offset < (src_height / tile_size):
                print(
                    f"Generating Tile[{self.zoom}]: {x_offset} (of {(src_width / tile_size)}) / {y_offset} (of {(src_height / tile_size)})")
                tile = src_img.crop((x_offset * tile_size,
                                     y_offset * tile_size,
                                     x_offset * tile_size + tile_size,
                                     y_offset * tile_size + tile_size))
                if not tile_empty(tile):
                    tile.save(f"{self.tiles_path}/{self.zoom}/{x_offset + self.x_min}/{y_offset + self.y_min}.png")
                y_offset += 1

            x_offset += 1

    def run(self):
        self.create_reference_points()
        self.prepare_coordinates_for_warp()
        self.warp_image()
        self.generate_tiles()


if __name__ == "__main__":
    for zoom in range(13, 19):
        generator = GenerateTiles("tiles", 'input/overlayPicture.png', zoom)
        generator.run()
