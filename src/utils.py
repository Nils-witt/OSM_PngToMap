import multiprocessing

import math
from PIL import Image


# Credits: https://wiki.openstreetmap.org/wiki/Slippy_map_tilenames#Python
def deg2num(lat_deg, lon_deg, zoom):
    lat_rad = math.radians(lat_deg)
    n = 1 << zoom
    x_tile = (lon_deg + 180.0) / 360.0 * n
    y_tile = (1.0 - math.asinh(math.tan(lat_rad)) / math.pi) / 2.0 * n
    return x_tile, y_tile


# Credits: https://wiki.openstreetmap.org/wiki/Slippy_map_tilenames#Python
def num2deg(x_tile, y_tile, zoom):
    n = 1 << zoom
    lon_deg = x_tile / n * 360.0 - 180.0
    lat_rad = math.atan(math.sinh(math.pi * (1 - 2 * y_tile / n)))
    lat_deg = math.degrees(lat_rad)
    return lat_deg, lon_deg


def tile_empty(tile) -> bool:
    for x in range(0, tile.width):
        for y in range(0, tile.height):
            if tile.getpixel((x, y)) != (0, 0, 0, 0):
                return False
    return True


def find_y_bounds(src_img: Image) -> int:
    src_height = src_img.height
    src_width = src_img.width
    found_pixel = False
    print(src_img.mode)

    y = src_height - 1
    if src_img.mode == "RGBA":
        while not found_pixel and y > 0:
            for x in range(0, src_width, 1):
                if src_img.getpixel((x, y)) != (0, 0, 0, 0):
                    found_pixel = True
            y = y - 256

    elif src_img.mode == "RGB":
        while not found_pixel and y > 0:
            for x in range(0, src_width, 1):
                if src_img.getpixel((x, y)) != (0, 0, 0):
                    found_pixel = True
            y = y - 256

    return y + (256 * 2)


def find_x_bounds(src_img: Image) -> int:
    src_height = src_img.height
    src_width = src_img.width
    found_pixel = False

    x = src_width - 1
    if src_img.mode == "RGBA":
        while not found_pixel and x > 0:
            for y in range(0, src_height, 1):
                if src_img.getpixel((x, y)) != (0, 0, 0, 0):
                    found_pixel = True
            x = x - 256
    elif src_img.mode == "RGB":
        while not found_pixel and x > 0:
            for y in range(0, src_height, 1):
                if src_img.getpixel((x, y)) != (0, 0, 0):
                    found_pixel = True
            x = x - 256
    return x + (256 * 2)
