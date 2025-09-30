"""
main.py

This is the main script to run the map tile generation pipeline from the command line.
"""

import os
import sys

os.environ["OPENCV_IO_MAX_IMAGE_PIXELS"] = pow(2, 40).__str__()

import entry
from tile_calc import resize, create_index_json


def main():
    """
    Main function to parse command-line arguments and run the tile generation and processing pipeline.
    """
    if len(sys.argv) < 6:
        print("Usage: python main.py <project_directory> <input_image> <config> <max_zoom_level> <min_zoom_level>")
        sys.exit(1)
    print(sys.argv)
    work_path = sys.argv[1]
    input_image = sys.argv[2]
    config = sys.argv[3]

    max_zoom_level = int(sys.argv[4])
    min_zoom_level = int(sys.argv[5])
    if not os.path.exists(f'{work_path}'):
        print(f"Project directory '{work_path}' does not exist.")
        sys.exit(1)
    if not os.path.exists(f'{input_image}'):
        print(f"Input image '{input_image}' does not exist.")
        sys.exit(1)
    if not os.path.exists(f'{config}'):
        print(f"Input image '{config}' does not exist.")
        sys.exit(1)

    tile_path = os.path.join(work_path, "tiles")
    tmp_path = os.path.join(work_path, "tmp")

    # create_index_json(output_path)

    print(f"Starting processing for project '{work_path}' with input image '{input_image} and {config}'...")
    entry.main(tile_path=tile_path, tmp_path=tmp_path, image_path=input_image, config_path=config, zoom_levels=[max_zoom_level])
    print(f"Creating canvas for zoom level {max_zoom_level}...")
    #    create_canvas(output_path, max_zoom_level)

    for i in range(max_zoom_level - 1, min_zoom_level - 1, -1):
        print(f"Resizing zoom level to {i}...")
        resize(tile_path, i)
        print(f"Creating canvas for zoom level {i}...")
        #       create_canvas(output_path, i)
        print(f"Done for zoom level {i}.")
    create_index_json(tile_path)


if __name__ == "__main__":
    main()
