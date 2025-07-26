import os
import sys

import entry
from tile_calc import create_canvas, resize, create_index_json

DATA_DIR = "/Users/nilswitt/git/pngToMap/data/"


def main():
    if len(sys.argv) < 5:
        print("Usage: python main.py <project_directory> <input_image> <max_zoom_level> <min_zoom_level>")
        sys.exit(1)

    project_dir = sys.argv[1]
    input_image = sys.argv[2]
    max_zoom_level = int(sys.argv[3])
    min_zoom_level = int(sys.argv[4])
    if not os.path.exists(f'{DATA_DIR}/{project_dir}'):
        print(f"Project directory '{DATA_DIR}/{project_dir}' does not exist.")
        sys.exit(1)
    if not os.path.exists(f'{DATA_DIR}/{project_dir}/input/{input_image}'):
        print(f"Input image '{input_image}' does not exist.")
        sys.exit(1)

    print(f"Starting processing for project '{project_dir}' with input image '{input_image}'...")
    entry.main(project_name=project_dir, image_path=input_image, data_dir=DATA_DIR, zoom_levels=[max_zoom_level])
    print(f"Creating canvas for zoom level {max_zoom_level}...")
    create_canvas(f'{DATA_DIR}/{project_dir}/output', max_zoom_level)
    create_index_json(f'{DATA_DIR}/{project_dir}/output', max_zoom_level)
    for i in range(max_zoom_level - 1, min_zoom_level - 1, -1):
        print(f"Resizing zoom level to {i}...")
        resize(f'{DATA_DIR}/{project_dir}/output', i)
        print(f"Creating canvas for zoom level {i}...")
        create_canvas(f'{DATA_DIR}/{project_dir}/output', i)
        print(f"Done for zoom level {i}.")
        create_index_json(f'{DATA_DIR}/{project_dir}/output', i)

if __name__ == "__main__":
    main()
