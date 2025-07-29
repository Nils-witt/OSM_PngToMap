import json
import logging
import os
import shutil

from PIL import Image

from create_marker_overlay import GenerateTiles

Image.MAX_IMAGE_PIXELS = None

USE_CACHE = False


def main(output_path: str, image_path: str, config_path: str, zoom_levels: list):
    working_dir = os.path.join(output_path, "workdir")

    print("Input directory: {}".format(image_path))
    print("Config path: {}".format(config_path))
    print("Working directory: {}".format(working_dir))
    print("Output directory: {}".format(output_path))
    if not os.path.exists(working_dir):
        os.makedirs(working_dir, exist_ok=True)

    if not os.path.exists(os.path.join(image_path)):
        print("Missing input image")
        exit(1)

    if image_path.endswith(".pdf"):
        print("Converting PDF to PNG not implemented yet")
        exit(1)

    elif image_path.endswith(".png"):
        shutil.copyfile(image_path, os.path.join(working_dir, "tmp.png"))
        print("Image is already a PNG, skipping conversion.")

    tmp_img_path = os.path.join(working_dir, "tmp.png")
    tmp_cleand_img_path = os.path.join(working_dir, "tmp_cleaned.png")
    img = Image.open(tmp_img_path)
    img.save(tmp_cleand_img_path)
    print("Done: Removing parts of the image")
    del img
    print("STEP 3: Sizing image to max input size")
    img = Image.open(tmp_cleand_img_path)

    if img.width > 32766 or img.height > 32766:
        print("Image too large, resizing to 32766")
        if img.width > img.height:
            wpercent = (32766 / float(img.size[0]))
            hsize = int((float(img.size[1]) * float(wpercent)))
            print(f"Resizing image to {32766}x{hsize}")
            img = img.resize((32766, hsize))
            img.save(tmp_cleand_img_path)
        else:
            pass
    if not os.path.exists(config_path):
        print("Missing input config")
        exit(1)

    print("STEP 4: Loading config and scaling markers")
    f = open(config_path)
    config = json.loads(f.read())
    f.close()

    imgsize = img.size
    print("Ref: Imfage size: {}".format(imgsize))
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
    logging.basicConfig(filename=f'{output_path}/tile.log', level=logging.INFO)
    os.makedirs(os.path.join(working_dir, "generator"), exist_ok=True)
    zoom_max = max(zoom_levels)

    print("STEP 4: Run Generator")
    generator = GenerateTiles(
        output_path,
        os.path.join(working_dir, "tmp_cleaned.png"),
        markers_scaled,
        zoom=zoom_max,
        logger=logger,
        tmp_dir=os.path.join(working_dir, "generator"),
    )
    generator.run()
