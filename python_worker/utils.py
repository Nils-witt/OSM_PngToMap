"""
utils.py

This module provides utility functions for coordinate conversions, tile checks, and image boundary detection.
"""

import math

import numpy as np
from PIL import Image


# Credits: https://wiki.openstreetmap.org/wiki/Slippy_map_tilenames#Python
def deg2num(lat_deg, lon_deg, zoom):
    """
    Converts latitude and longitude to OSM tile numbers at a given zoom level.
    """
    lat_rad = math.radians(lat_deg)
    n = 1 << zoom
    x_tile = (lon_deg + 180.0) / 360.0 * n
    y_tile = (1.0 - math.asinh(math.tan(lat_rad)) / math.pi) / 2.0 * n
    return x_tile, y_tile


# Credits: https://wiki.openstreetmap.org/wiki/Slippy_map_tilenames#Python
def num2deg(x_tile, y_tile, zoom):
    """
    Converts OSM tile numbers to latitude and longitude at a given zoom level.
    """
    n = 1 << zoom
    lon_deg = x_tile / n * 360.0 - 180.0
    lat_rad = math.atan(math.sinh(math.pi * (1 - 2 * y_tile / n)))
    lat_deg = math.degrees(lat_rad)
    return lat_deg, lon_deg


def tile_empty(tile) -> bool:
    """
    Checks if a tile image is completely transparent (empty).
    """
    return not np.asarray(tile).any()


def find_y_bounds(src_img: Image) -> int:
    """
    Finds the lower y-bound of non-transparent pixels in the image.
    """
    arr = np.asarray(src_img)

    y = src_img.height - 1
    while y > 0 and not arr[y].any():
        y -= 256

    return y + (256 * 2)


def find_x_bounds(src_img: Image) -> int:
    """
    Finds the right x-bound of non-transparent pixels in the image.
    """
    arr = np.asarray(src_img)

    x = src_img.width - 1
    while x > 0 and not arr[:, x].any():
        x -= 256

    return x + (256 * 2)
