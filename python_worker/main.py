import argparse
import json
import os
from pathlib import Path

from PIL import Image

from create_marker_overlay import GenerateTiles
from tile_calc import resize


def create_directories(config_dir: Path):
    if not config_dir.exists():
        os.mkdir(config_dir)

    tiles_dir = config_dir / "tiles"
    if not tiles_dir.exists():
        os.mkdir(tiles_dir)

    tmp_dir = config_dir / "tmp"
    if not tmp_dir.exists():
        os.mkdir(tmp_dir)


def read_config(config_dir: Path):
    with open(config_dir / "config.json") as config_file:
        config = json.load(config_file)
    return config


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Python Worker")
    parser.add_argument(
        "--config-dir",
        type=Path,
        default=Path("config"),
        help="Directory containing configuration files (default: %(default)s)",
    )
    parser.add_argument(
        "--max-zoom",
        type=int,
        default=18,
        help="Maximum zoom level (default: %(default)s)",
    )
    parser.add_argument(
        "--min-zoom",
        type=int,
        default=14,
        help="Minimum zoom level (default: %(default)s)",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    print(f"Hello from Python Worker! Using config directory: {args.config_dir}")
    config = read_config(args.config_dir)
    print("Config loaded:", config)
    create_directories(args.config_dir)

    with Image.open(args.config_dir / "image.png") as img:
        imgsize = img.size

    markers_scaled = {}
    print(config['coordinates'])
    if len(config['coordinates']) < 4:
        print("Not enough coordinates")
        return -1

    for i in range(0, 4):
        scale_width = imgsize[0] / config['img_scale']['width']
        scale_height = imgsize[1] / config['img_scale']['height']
        markers_scaled[i] = {
            "overlay": {
                "x": config['coordinates'][i]['img']['x'] * scale_width,
                "y": config['coordinates'][i]['img']['y'] * scale_height
            },
            "map": {
                "lat": config['coordinates'][i]['map']['latitude'],
                "lng": config['coordinates'][i]['map']['longitude']
            }
        }

    generator = GenerateTiles(
        args.config_dir / "tiles",
        args.config_dir / "image.png",
        markers_scaled,
        zoom=args.max_zoom,
        tmp_dir=args.config_dir / "tmp",
    )
    generator.run()

    for i in range(args.max_zoom - 1, args.min_zoom - 1, -1):
        print(f"Resizing to {i}")
        resize(args.config_dir / "tiles", i)
    return None


if __name__ == "__main__":
    main()
