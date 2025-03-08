import os.path
from os import listdir

from PIL import Image


def main():
    zoom = 17
    mypath = "basemap/" + str(zoom)
    x_values = [68115, 68134]
    y_values = [44024,44052]
    '''
    for dir_name in listdir(mypath):
        x_values.append(int(dir_name))
        for file_name in listdir(mypath + "/" + dir_name):
            val = int(file_name.split(".")[0])
            if not val in y_values:
                y_values.append(val)
    x_values.sort()
    y_values.sort()
    '''
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
