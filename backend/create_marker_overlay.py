"""
create_marker_overlay.py

This module provides the GenerateTiles class, which handles the process of overlaying marker data onto map tiles,
warping and cropping the overlay image, and generating map tiles for use in mapping applications.
"""

import multiprocessing
import os

import cv2
import numpy as np
from PIL import Image
from PIL.Image import DecompressionBombError

from utils import deg2num, find_x_bounds, find_y_bounds, tile_empty

Image.MAX_IMAGE_PIXELS = None


class GenerateTiles:
    """
    GenerateTiles handles the process of generating map tiles from an overlay image and marker data.
    """

    coordinates: list[list[float]] = []
    picture_points: list[list[int]] = []

    def __init__(
            self,
            tiles_path: str,
            overlay_img_path: str,
            markers: {},
            zoom: int,
            logger=None,
            tmp_dir: str = "tmp/"
    ):
        """
        Initialize the GenerateTiles object with paths, marker data, zoom level, logger, and temp directory.
        """
        self.map_img_offsets = None
        self.x_max = None
        self.x_min = None
        self.y_max = None
        self.y_min = None
        self.tiles_path = tiles_path
        self.overlay_img_path = overlay_img_path
        self.zoom = zoom
        self.logger = logger
        self.markers = markers
        self.tmp_dir = tmp_dir

    def create_reference_points(self):
        """
        Extracts reference points from the markers for both map coordinates and overlay image points.
        """
        self.coordinates: list[list[float]] = [[self.markers[f]['map']['lat'], self.markers[f]['map']['lng']] for f in
                                               self.markers]
        for coord in self.coordinates:
            print("loaded coordinate", coord)
        self.picture_points: list[list[int]] = [[self.markers[f]['overlay']['x'], self.markers[f]['overlay']['y']] for f
                                                in self.markers]
        for point in self.picture_points:
            print("Loaded picture point", point)

    def prepare_coordinates_for_warp(self):
        """
        Prepares the coordinates and calculates the bounds for warping the overlay image to map tiles.
        """

        marker_osm_tiles = [deg2num(coord[0], coord[1], self.zoom) for coord in self.coordinates]
        # Compute Tiles
        x_tiles = [int(f[0]) for f in marker_osm_tiles]
        y_tiles = [int(f[1]) for f in marker_osm_tiles]
        x_tiles.sort()
        y_tiles.sort()

        osm_tile_offset = 20

        self.y_min = y_tiles[0] - osm_tile_offset
        self.y_max = y_tiles[-1] + osm_tile_offset
        self.x_min = x_tiles[0] - osm_tile_offset
        self.x_max = x_tiles[-1] + osm_tile_offset

        self.logger.info(
            f"X-Tile-Bounds[{self.zoom}]: max: {self.x_max} min: {self.x_min}, count : {self.x_max - self.x_min + 1}")
        self.logger.info(
            f"Y-Tile-Bounds[{self.zoom}]:max: {self.y_max} min: {self.y_min}, count : {self.y_max - self.y_min + 1}")

        for (i, val) in enumerate(marker_osm_tiles):
            self.logger.info(
                f"[Marker {i + 1}][{self.zoom}] Overlay [{self.picture_points[i][0]}, {self.picture_points[i][1]}] Map [{(val[0] - self.x_min) * 256}, {(val[1] - self.y_min) * 256}]")

        self.map_img_offsets = [(int((val[0] - self.x_min) * 256), int((val[1] - self.y_min) * 256)) for val in
                                marker_osm_tiles]

        self.logger.info(f"Map Image Offsets: {self.map_img_offsets}")

    def calulate_target_size(self, ):
        """
        Calculates the target size for the warped overlay image based on tile bounds.
        """
        return (
            (self.x_max - self.x_min) * 256,
            (self.y_max - self.y_min) * 256
        )

    def warp_image(self):
        """
        Warps the overlay image using homography based on reference points and saves the result.
        """
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
        print("PIXEL:" + str(im_src[0,0]))
        target_pic_size = self.calulate_target_size()

        im_out = cv2.warpPerspective(
            im_src,
            h,
            target_pic_size,
            borderMode=cv2.BORDER_TRANSPARENT
        )
        del im_src
        cv2.imwrite(f"{self.tmp_dir}/overlay_{self.zoom}.png", im_out)
        del im_out

    def crop_image(self):
        """
        Crops the warped overlay image to remove empty space and saves the cropped image.
        """
        self.logger.info("Cropping image")
        if os.path.exists(f"{self.tmp_dir}/overlay_{self.zoom}_crop.png"):
            self.logger.info("Skipping crop, already exists")
            return
        src_img = Image.open(f"{self.tmp_dir}/overlay_{self.zoom}.png")
        lower_y = find_y_bounds(src_img)
        print("YL:", lower_y)
        right_x = find_x_bounds(src_img)
        print("XR:", right_x)
        cropped = src_img.crop((0, 0, right_x, lower_y))
        cropped.save(f"{self.tmp_dir}/overlay_{self.zoom}_crop.png")
        del cropped
        self.logger.info("Copping image done")

    def tile_worker(self, img: Image, x_offset: int, y_offset: int, save_path: str):
        """
        Worker function to crop a single tile from the image and save it if not empty.
        """
        tile_size = 256
        tile = img.crop((x_offset * tile_size,
                         y_offset * tile_size,
                         x_offset * tile_size + tile_size,
                         y_offset * tile_size + tile_size))
        if not tile_empty(tile):
            tile.save(save_path)

    def tile_x_worker(self, img: Image, x_offset: int):
        """
        Worker function to process all tiles in a given x column.
        """
        tile_size = 256
        current_x_dir: str = f"{self.tiles_path}/{self.zoom}/{x_offset + self.x_min}"
        os.makedirs(current_x_dir, exist_ok=True)
        y_offset = 0
        while y_offset < (img.height / tile_size):
            self.tile_worker(img, x_offset, y_offset, f"{current_x_dir}/{y_offset + self.y_min}.png")
            y_offset += 1
        if len(os.listdir(current_x_dir)) == 0:
            os.rmdir(current_x_dir)

    def tile_x_queues_worker(self, img: Image, queue: list[int]):
        """
        Worker function to process a queue of x columns for tiling.
        """
        for i in queue:
            self.tile_x_worker(img, i)

    def generate_tiles(self):
        """
        Generates all map tiles from the cropped overlay image using multiprocessing.
        """
        try:
            src_img = Image.open(f"{self.tmp_dir}/overlay_{self.zoom}_crop.png")
            src_height = src_img.height
            src_width = src_img.width
        except DecompressionBombError:
            self.logger.error(f"DecompressionBombError")
            return

        self.logger.info(f"Src Image[{self.zoom}]: {src_width}, {src_height}")
        tile_size = 256
        cores = multiprocessing.cpu_count() - 1
#        cores = 2
        self.logger.info(f"Using {cores} cores")

        queues = {}
        for i in range(cores):
            queues[i] = []

        x_offset = 0
        while x_offset < (src_width / tile_size):
            queues[x_offset % cores].append(x_offset)
            x_offset += 1

        procs = {}
        for i in range(cores):
            p = multiprocessing.Process(target=self.tile_x_queues_worker, args=(src_img, queues[i]))
            print(f"Starting process {i}")
            p.start()
            procs[i] = p
            #self.tile_x_queues_worker(src_img, queues[i])

        for i in range(cores):
            procs[i].join()
            print("Done process ", i)

        print("Done alle")

    def run(self):
        """
        Runs the complete tile generation pipeline: reference points, warp, crop, and tile generation.
        """
        self.logger.info("Starting")
        self.create_reference_points()
        self.prepare_coordinates_for_warp()
        self.warp_image()
        self.crop_image()
        self.generate_tiles()
        self.logger.info("Done")
