import json
import os.path

from PIL import Image

from utils import deg2num


def main():
    zoom = 17
    mypath = "basemap/" + str(zoom)
    with open('tmp/markers.json') as json_data:
        d = json.loads(json_data.read())
        json_data.close()
        coordinates: list[list[float]] = [[d[f]['map']['lat'], d[f]['map']['lng']] for f in d]
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

        new_im.save(f'out/{zoom}.png')


if __name__ == "__main__":
    main()
