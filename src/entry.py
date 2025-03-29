import logging
import os

import pymupdf
from PIL import Image

from create_marker_overlay import GenerateTiles

Image.MAX_IMAGE_PIXELS = None

DATA_DIR = "/Users/nilswitt/git/pngToMap/data/"
PROJECT_NAME = "Innenstadt"

ZOOM_LEVELS = range(15, 22)

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
    if not os.path.exists(os.path.join(project_dir + "output")):
        os.makedirs(os.path.join(project_dir + "output"), exist_ok=True)

    if not os.path.exists(os.path.join(project_dir, "input", "input.pdf")):
        print("Missing input image")
        exit(1)
    if not os.path.exists(os.path.join(project_dir, "input", "markers.json")):
        print("Missing input config")
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

    logger = logging.getLogger(__name__)
    logger.addHandler(logging.StreamHandler())
    logging.basicConfig(filename=f'{project_dir}/tile.log', level=logging.INFO)
    os.makedirs(os.path.join(working_dir, "generator"), exist_ok=True)
    for ZOOM_LEVEL in ZOOM_LEVELS:
        generator = GenerateTiles(
            os.path.join(project_dir, "output"),
            os.path.join(working_dir, "tmp.png"),
            os.path.join(project_dir, "input", "markers.json"),
            zoom=ZOOM_LEVEL,
            logger=logger,
            tmp_dir=os.path.join(working_dir, "generator"),
        )
        generator.run()


if __name__ == "__main__":
    main()
