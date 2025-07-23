import json
import os.path
from io import BytesIO

import requests
from PIL import Image

from utils import deg2num


def generate(data, zoom):
    mypath = "tmp/basemap/" + str(zoom)
    markers = data['markers']
    coordinates: list[list[float]] = [[markers[f]['map']['lat'], markers[f]['map']['lng']] for f in markers]
    osm_tiles = [deg2num(coord[0], coord[1], zoom) for coord in coordinates]
    # Compute Tiles
    x_tiles = [int(f[0]) for f in osm_tiles]
    y_tiles = [int(f[1]) for f in osm_tiles]

    x_tiles.sort()
    y_tiles.sort()

    y_min = y_tiles[0]
    y_max = y_tiles[-1]
    x_min = x_tiles[0]
    x_max = x_tiles[-1]

    x_values = [x_min, x_max]
    y_values = [y_min, y_max]

    print(f"Bounds: {x_values[0]}, {x_values[-1]}, {y_values[0]}, {y_values[-1]}")

    x = x_values[-1] - x_values[0] + 1
    y = y_values[-1] - y_values[0] + 1

    print(f"Dimensions: {x}, {y}")

    new_im = Image.new('RGB', (x * 256, y * 256))

    for (i, x_val) in enumerate(range(x_values[0], x_values[-1] + 1)):
        for (j, y_val) in enumerate(range(y_values[0], y_values[-1] + 1)):
            try:
                print(mypath + "/" + str(x_val) + "/" + str(y_val) + ".png => " + os.path.isfile(
                    mypath + "/" + str(x_val) + "/" + str(y_val) + ".png").__str__())

                im = Image.open(mypath + "/" + str(x_val) + "/" + str(y_val) + ".png")
                new_im.paste(im, (i * 256, j * 256))
            except:
                print(f"Could not find {x_val}, {y_val}")

    new_im.save(f'tmp/basemap_{zoom}.png')


def generate_osm_png(tile_url: str, x_min: int, x_max: int, y_min: int, y_max: int, zoom: int) -> Image:
    # Generate the OSM PNG file using the tile_url and the specified bounds
    # This function should implement the logic to download and save the PNG file
    width = x_max - x_min + 1
    height = y_max - y_min + 1

    new_im = Image.new('RGBA', (width * 256, height * 256))
    if zoom > 19:
        return new_im
    for i in range(0, width):
        for j in range(0, height):
            try:
                url = tile_url.replace("{z}", str(zoom)).replace("{x}", str(i + x_min)).replace("{y}", str(j + y_min))
                print(f"Downloading tile from {url}")
                response = requests.get(url)
                img = Image.open(BytesIO(response.content))
                img = img.convert('RGBA')
                new_im.paste(img, [i * 256, j * 256, (i + 1) * 256, (j + 1) * 256])
            except:
                print(f"Could not find {i}, {j}")
    return new_im


def main():
    with open('tmp/muenster/config.json') as json_data:
        d = json.loads(json_data.read())
        json_data.close()
        zooms = range(d['minZoom'], d['maxZoom'] + 1)
        for zoom in zooms:
            print("Generating tiles for zoom", zoom)
            generate(d, zoom)


if __name__ == "__main__":
    main()
