import math
import os

import cv2
import numpy as np
from PIL import Image


def deg2num(lat_deg, lon_deg, zoom):
    lat_rad = math.radians(lat_deg)
    n = 1 << zoom
    x_tile = (lon_deg + 180.0) / 360.0 * n
    y_tile = (1.0 - math.asinh(math.tan(lat_rad)) / math.pi) / 2.0 * n
    return x_tile, y_tile


def main():
    # Map Coordinates
    pos1 = deg2num(50.74887947353795, 7.115331888198853, 17)
    pos2 = deg2num(50.70164265976951, 7.136918306350709, 17)
    pos3 = deg2num(50.732425421722816, 7.085624870058269, 17)
    pos4 = deg2num(50.72491724166254, 7.151895761489869, 17)

    # Overlay Pixels
    pos1_pic = [310, 95]  # x, y
    pos2_pic = [4855, 2502]  # x, y
    pos3_pic = [172, 2709]  # x, y
    pos4_pic = [3802, 95]  # x, y

    # Compute Tiles
    x_tiles = [int(f[0]) for f in [pos1, pos2, pos3, pos4]]
    y_tiles = [int(f[1]) for f in [pos1, pos2, pos3, pos4]]
    x_tiles.sort()
    y_tiles.sort()
    y_min = y_tiles[0]
    y_max = y_tiles[-1]
    x_min = x_tiles[0]
    x_max = x_tiles[-1]
    print(f"Tiles: {x_tiles} max: {x_max} min: {x_min}")
    print(f"Tiles: {y_tiles} max: {y_max} min: {y_min}")

    print(
        f"[Marker 1] Overlay [{pos1_pic[0]}, {pos1_pic[1]}] Map [{(pos1[0] - x_min) * 256}, {(pos1[1] - y_min) * 256}]")
    print(
        f"[Marker 2] Overlay [{pos2_pic[0]}, {pos2_pic[1]}] Map [{(pos2[0] - x_min) * 256}, {(pos2[1] - y_min) * 256}]")
    print(
        f"[Marker 3] Overlay [{pos3_pic[0]}, {pos3_pic[1]}] Map [{(pos3[0] - x_min) * 256}, {(pos3[1] - y_min) * 256}]")
    print(
        f"[Marker 4] Overlay [{pos4_pic[0]}, {pos4_pic[1]}] Map [{(pos4[0] - x_min) * 256}, {(pos4[1] - y_min) * 256}]")

    pos1_map_offset = [(pos1[0] - x_min) * 256, (pos1[1] - y_min) * 256]
    pos2_map_offset = [(pos2[0] - x_min) * 256, (pos2[1] - y_min) * 256]
    pos3_map_offset = [(pos3[0] - x_min) * 256, (pos3[1] - y_min) * 256]
    pos4_map_offset = [(pos4[0] - x_min) * 256, (pos4[1] - y_min) * 256]

    pts_src = np.array([pos1_pic, pos2_pic, pos3_pic, pos4_pic])
    pts_dst = np.array([pos1_map_offset, pos2_map_offset, pos3_map_offset, pos4_map_offset])

    h, status = cv2.findHomography(pts_src, pts_dst)

    im_src = cv2.imread('input/overlayPicture.png', cv2.IMREAD_UNCHANGED)
    im_dst = cv2.imread('out/17.png')

    im_out = cv2.warpPerspective(im_src, h, (im_dst.shape[1] * 2, im_dst.shape[0] * 2))

    cv2.imwrite("out/output.png", im_out)


def create_tiles():

    zoom = 17
    pos1 = deg2num(50.74887947353795, 7.115331888198853, zoom)
    pos2 = deg2num(50.70164265976951, 7.136918306350709, zoom)
    pos3 = deg2num(50.732425421722816, 7.085624870058269, zoom)
    pos4 = deg2num(50.72491724166254, 7.151895761489869, zoom)
    print(f"pos1: {pos1}")
    x_tiles = [int(f[0]) for f in [pos1, pos2, pos3, pos4]]
    y_tiles = [int(f[1]) for f in [pos1, pos2, pos3, pos4]]
    x_tiles.sort()
    y_tiles.sort()
    y_min = y_tiles[0]
    y_max = y_tiles[-1]
    x_min = x_tiles[0]
    x_max = x_tiles[-1]
    print(f"Tiles: {x_tiles} max: {x_max} min: {x_min}")
    print(f"Tiles: {y_tiles} max: {y_max} min: {y_min}")

    pos1_map_offset = [(pos1[0] - x_min) * 256, (pos1[1] - y_min) * 256]
    pos2_map_offset = [(pos2[0] - x_min) * 256, (pos2[1] - y_min) * 256]
    pos3_map_offset = [(pos3[0] - x_min) * 256, (pos3[1] - y_min) * 256]
    pos4_map_offset = [(pos4[0] - x_min) * 256, (pos4[1] - y_min) * 256]

    src_img = Image.open("out/output.png")

    src_height = src_img.height
    src_width = src_img.width

    print(f"Src Image: {src_width}, {src_height}")

    x_offset = 0

    while x_offset < (src_width /256):
        os.makedirs(f"tiles/{zoom}/{x_offset + x_min}", exist_ok=True)
        y_offset = 0
        while y_offset < (src_height/256):
            print(f"Generating Tile: {x_offset} (of {(src_width /256)}) / {y_offset} (of {(src_height /256)})")
            tile = src_img.crop((x_offset * 256, y_offset * 256, x_offset * 256 + 256, y_offset * 256 + 256))
            tile.save(f"tiles/{zoom}/{x_offset + x_min}/{y_offset + y_min}.png")
            y_offset += 1

        x_offset += 1


if __name__ == "__main__":
    # main()
    create_tiles()
