"""
entry.py

This module provides the main entry point for processing an input image and configuration to generate map tiles.
"""

import json
import logging
import os
import shutil

from PIL import Image

from create_marker_overlay import GenerateTiles

Image.MAX_IMAGE_PIXELS = None

USE_CACHE = False


def main(tile_path: str, tmp_path: str, image_path: str, config_path: str, zoom_levels: list):
    """
    Main function to process the input image and configuration, scale markers, and generate map tiles.
    """

    tmp_img_path = os.path.join(tmp_path, "tmp.png")

    print("Input directory: {}".format(image_path))
    print("Config path: {}".format(config_path))
    print("Working directory: {}".format(tmp_path))
    print("Tile directory: {}".format(tile_path))
    if not os.path.exists(tmp_path):
        os.makedirs(tmp_path, exist_ok=True)
    if not os.path.exists(tile_path):
        os.makedirs(tile_path, exist_ok=True)

    if not os.path.exists(image_path):
        print("Missing input image")
        exit(1)

    if os.path.exists(tmp_img_path):
        print("Using cached image")
    elif image_path.endswith(".pdf"):
        print("Converting PDF to PNG not implemented yet")
        exit(1)

    elif image_path.endswith(".png"):
        shutil.copyfile(image_path, tmp_img_path)
        print("Image is already a PNG, skipping conversion.")
    elif image_path.endswith(".jpg"):
        img = Image.open(image_path)
        converted = img.convert("RGBA")
        converted.save(tmp_img_path)

        print("Converted JPG to PNG.")
    print("Done: Removing parts of the image")
    print("STEP 3: Sizing image to max input size")
    img = Image.open(tmp_img_path)
    print(f"Image Mode: {img.mode}")

    if img.width > 32766 or img.height > 32766:
        print("Image too large, resizing to 32766")
        if img.width > img.height:
            print("Resizing width")
            wpercent = (32766 / float(img.size[0]))
            hsize = int((float(img.size[1]) * float(wpercent)))
            print(f"Resizing image to {32766}x{hsize}")
            img = img.resize((32766, hsize))
            img.save(tmp_img_path)
        else:
            print("Resizing height")
            hpercent = (32766 / float(img.size[1]))
            wsize = int((float(img.size[0]) * float(hpercent)))
            print(f"Resizing image to {wsize}x{32766}")
            img = img.resize((wsize, 32766))
            img.save(tmp_img_path)
    if not os.path.exists(config_path):
        print("Missing input config")
        exit(1)

    print("STEP 4: Loading config and scaling markers")
    f = open(config_path)
    config = json.loads(f.read())
    f.close()

    imgsize = img.size
    print("Ref: Image size: {}".format(imgsize))
    scale_width = imgsize[0] / config['img_scale']['width']
    scale_height = imgsize[1] / config['img_scale']['height']
    del img

    markers_scaled = {}
    for i in range(1, 5):
        markers_scaled[i] = {
            "overlay": {
                "x": config['img'][i.__str__()]['x'] * scale_width,
                "y": config['img'][i.__str__()]['y'] * scale_height
            },
            "map": {
                "lat": config['map'][i.__str__()]['latitude'],
                "lng": config['map'][i.__str__()]['longitude']
            }
        }
    print(f"Scale: {scale_width}, {scale_height}")

    print("Markers on input image:")
    for i in range(1, 5):
        print(f"M{i}: {markers_scaled[i]['overlay']['x']}, {markers_scaled[i]['overlay']['y']}")

    logger = logging.getLogger(__name__)
    logger.addHandler(logging.StreamHandler())
    logging.basicConfig(filename=f'{tmp_path}/tile.log', level=logging.INFO)
    os.makedirs(os.path.join(tmp_path, "generator"), exist_ok=True)
    zoom_max = max(zoom_levels)

    print("STEP 5: Run Generator")

    generator = GenerateTiles(
        tile_path,
        tmp_img_path,
        markers_scaled,
        zoom=zoom_max,
        logger=logger,
        tmp_dir=os.path.join(tmp_path, "generator"),
    )
    generator.run()
