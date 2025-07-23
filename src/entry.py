import json
import logging
import os

import pymupdf
from PIL import Image

from create_marker_overlay import GenerateTiles

Image.MAX_IMAGE_PIXELS = None

DATA_DIR = "/Users/nilswitt/git/pngToMap/data/"
PROJECT_NAME = "Innenstadt"

ZOOM_LEVELS = range(10, 15 + 1)

USE_CACHE = False
"""
Assertions
PDF has one page and there is the image on the first page
"""
def main():
    project_dir = os.path.join(DATA_DIR, PROJECT_NAME)
    working_dir = os.path.join(project_dir, "workdir")

    if not os.path.exists(project_dir):
        os.makedirs(project_dir, exist_ok=True)
    if not os.path.exists(os.path.join(project_dir, "input")):
        os.makedirs(os.path.join(project_dir, "input"), exist_ok=True)
    if not os.path.exists(working_dir):
        os.makedirs(working_dir, exist_ok=True)
    if not os.path.exists(os.path.join(project_dir, "output")):
        os.makedirs(os.path.join(project_dir, "output"), exist_ok=True)

    if not os.path.exists(os.path.join(project_dir, "input", "input.pdf")):
        print("Missing input image")
        exit(1)
    if not os.path.exists(os.path.join(working_dir, "tmp.png")):
        print(f"File not found: {working_dir}/tmp.png starting conversion.")
        doc = pymupdf.open(os.path.join(project_dir, "input", "input.pdf"))
        page = doc.load_page(0)
        pixmap = page.get_pixmap(dpi=700, alpha=True)
        pixmap.save(os.path.join(working_dir, "tmp.png"))
        print("Conversion done.")
    else:
        print("tmp.png already exists, skipping conversion.")

    if not os.path.exists(os.path.join(working_dir, "tmp_cleaned.png")):
        img = Image.open(os.path.join(working_dir, "tmp.png"))
        img.save(os.path.join(working_dir, "tmp_cleaned.png"))
        print("Done: Removing parts of the image")
        del img

    img = Image.open(os.path.join(working_dir, "tmp_cleaned.png"))

    if img.width > 32766 or img.height > 32766:
        print("Image too large, resizing to 32766")
        if img.width > img.height:
            wpercent = (32766 / float(img.size[0]))
            hsize = int((float(img.size[1]) * float(wpercent)))
            print(f"Resizing image to {32766}x{hsize}")
            img = img.resize((32766, hsize))
            img.save(os.path.join(working_dir, "tmp_cleaned.png"))
        else:
            pass

    if img.width > 2000 or img.height > 2000:
        print(f"Image is larger than 2000x2000 {img.width}x{img.height}")
        c_width = int(img.width / 2)
        c_height = int(img.height / 2)

        while(c_width > 2000 or c_height > 2000):
            print(f"Resizing image to {c_width}x{c_height}")
            if not os.path.exists(os.path.join(working_dir, f"overlay_{c_width}x{c_height}.png")):
                img_part = img.resize((int(c_width), c_height))
                img_part.save(os.path.join(working_dir, f"overlay_{c_width}x{c_height}.png"))
                del img_part
            else:
                print(f"Skipped")
            c_width = int(c_width / 2)
            c_height = int(c_height / 2)

    if not os.path.exists(os.path.join(project_dir, "input", "markers.json")):
        print("Missing input config")
        exit(1)

    f = open(os.path.join(project_dir,  "input", "markers.json"))
    config = json.loads(f.read())
    f.close()

    imgsize = img.size
    scale_width = imgsize[0] / config['image']['width']
    scale_height = imgsize[1] / config['image']['height']
    del img
    markers = config['markers']
    markers_scaled = {}
    for i in markers:
        markers_scaled[i] = {
            "overlay": {
                "x": markers[i]['overlay']['x'] * scale_width,
                "y": markers[i]['overlay']['y'] * scale_height
            },
            "map": {
                "lat": markers[i]['map']['lat'],
                "lng": markers[i]['map']['lng']
            }
        }
    print(f"Scale: {scale_width}, {scale_height}")
    for i in markers:
        print(f"M{i}: {markers[i]['overlay']['x']}, {markers[i]['overlay']['y']}")
        print(f"M{i}: {markers_scaled[i]['overlay']['x']}, {markers_scaled[i]['overlay']['y']}")

    logger = logging.getLogger(__name__)
    logger.addHandler(logging.StreamHandler())
    logging.basicConfig(filename=f'{project_dir}/tile.log', level=logging.INFO)
    os.makedirs(os.path.join(working_dir, "generator"), exist_ok=True)
    for ZOOM_LEVEL in ZOOM_LEVELS:
        generator = GenerateTiles(
            os.path.join(project_dir, "output"),
            os.path.join(working_dir, "tmp_cleaned.png"),
            markers_scaled,
            zoom=ZOOM_LEVEL,
            logger=logger,
            tmp_dir=os.path.join(working_dir, "generator"),
        )
        generator.run()


if __name__ == "__main__":
    main()
