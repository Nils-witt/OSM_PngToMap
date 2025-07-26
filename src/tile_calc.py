import os

from PIL import Image

from utils import num2deg, deg2num
import json


def resize(tile_path: str, target_zoom: int) -> None:
    tiles = []
    new_tiles_set = {}

    x_dirs = os.listdir(f"{tile_path}/{target_zoom + 1}")
    for x_dir in x_dirs:
        if not os.path.isdir(f"{tile_path}/{target_zoom + 1}/{x_dir}"):
            continue
        y_tiles = os.listdir(f"{tile_path}/{target_zoom + 1}/{x_dir}")
        for y_tile in y_tiles:
            if y_tile.endswith(".png"):
                tiles.append((int(x_dir), int(y_tile[:-4])))

    if not os.path.exists(f"{tile_path}/{target_zoom}"):
        os.makedirs(f"{tile_path}/{target_zoom}")

    for tile in tiles:
        coords = num2deg(tile[0], tile[1], target_zoom + 1)
        new_tiles = deg2num(coords[0], coords[1], target_zoom)

        current_tile_path = f"{tile_path}/{target_zoom + 1}/{tile[0]}/{tile[1]}.png"
        resized_tile_path = f"{tile_path}/{target_zoom}/{int(new_tiles[0])}/{int(new_tiles[1])}.png"

        bounds_x = int((new_tiles[0] - int(new_tiles[0])) * 512)
        bounds_y = int((new_tiles[1] - int(new_tiles[1])) * 512)

        if new_tiles_set.get(int(new_tiles[0])) is None:
            new_tiles_set[int(new_tiles[0])] = []
        new_tiles_set[int(new_tiles[0])].append(int(new_tiles[1]))

        with Image.open(current_tile_path) as tile_img:

            if not os.path.exists(f"{tile_path}/{target_zoom}/{int(new_tiles[0])}"):
                os.makedirs(f"{tile_path}/{target_zoom}/{int(new_tiles[0])}")

            if not os.path.exists(resized_tile_path):
                new_tile_img = Image.new("RGBA", (512, 512), "#00000000")  # Create a transparent image
                new_tile_img.paste(tile_img, (bounds_x, bounds_y))
                new_tile_img.save(resized_tile_path)
            else:
                new_tile_img = Image.open(resized_tile_path)
                new_tile_img.paste(tile_img, (bounds_x, bounds_y))
                new_tile_img.save(resized_tile_path)

    for x_new_tile in new_tiles_set:
        for y_new_tile in new_tiles_set[x_new_tile]:
            with (Image.open(
                    f"{tile_path}/{target_zoom}/{x_new_tile}/{y_new_tile}.png") as tile_img):
                tile_img.resize((256, 256)).save(
                    f"{tile_path}/{target_zoom}/{x_new_tile}/{y_new_tile}.png")


def create_canvas(data_dir: str, target_zoom: int) -> None:
    x_min = None
    y_min = None
    x_max = None
    y_max = None

    for x_dir in os.listdir(f"{data_dir}/{target_zoom}"):
        if not os.path.isdir(f"{data_dir}/{target_zoom}/{x_dir}"):
            continue
        x_value = int(x_dir)
        if x_min is None or x_min > x_value:
            x_min = x_value
        if x_max is None or x_max < x_value:
            x_max = x_value
        for y_dir in os.listdir(f"{data_dir}/{target_zoom}/{x_dir}"):
            y_value = int(y_dir[:-4])
            if y_min is None or y_min > y_value:
                y_min = y_value
            if y_max is None or y_max < y_value:
                y_max = y_value
    print("Z: ", target_zoom, "X: ", x_min, " - ", x_max, "Y: ", y_min, " - ", y_max)
    canvas = Image.new("RGBA", ((1 + x_max - x_min) * 256, (1 + y_max - y_min) * 256), (255, 0, 0, 0))

    for x_value in range(x_min, x_max + 1):
        x_offset = (x_value - x_min) * 256
        for y_value in range(y_min, y_max + 1):
            y_offset = (y_value - y_min) * 256
            tile_path = f"{data_dir}/{target_zoom}/{x_value}/{y_value}.png"
            if os.path.exists(tile_path):
                with Image.open(tile_path) as tile_img:
                    pass
                    canvas.paste(tile_img, (x_offset, y_offset), tile_img)
    canvas.save(f"{data_dir}/{target_zoom}/canvas.png")

def create_index_json(data_dir: str, target_zoom: int) -> None:
    index = {
        "zoom": target_zoom,
        "tiles": []
    }

    for x_dir in os.listdir(f"{data_dir}/{target_zoom}"):
        if not os.path.isdir(f"{data_dir}/{target_zoom}/{x_dir}"):
            continue
        x_value = int(x_dir)
        for y_dir in os.listdir(f"{data_dir}/{target_zoom}/{x_dir}"):
            y_value = int(y_dir[:-4])
            index["tiles"].append({
                "x": x_value,
                "y": y_value
            })

    with open(f"{data_dir}/{target_zoom}/index.json", "w") as f:
        json.dump(index, f, indent=4)