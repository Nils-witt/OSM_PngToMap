import json
import logging
import os
import shutil

from PIL import Image

from create_marker_overlay import GenerateTiles

Image.MAX_IMAGE_PIXELS = None

USE_CACHE = False

def main(project_name: str, image_path: str, data_dir: str, zoom_levels: list):
    project_dir = os.path.join(data_dir, project_name)
    working_dir = os.path.join(project_dir, "workdir")
    input_dir = os.path.join(project_dir, "input")
    output_dir = os.path.join(project_dir, "output")

    print("Project directory: {}".format(project_dir))
    print("Input directory: {}".format(input_dir))
    print("Working directory: {}".format(working_dir))
    print("Output directory: {}".format(output_dir))

    if not os.path.exists(project_dir):
        os.makedirs(project_dir, exist_ok=True)
    if not os.path.exists(input_dir):
        os.makedirs(input_dir, exist_ok=True)
    if not os.path.exists(working_dir):
        os.makedirs(working_dir, exist_ok=True)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)

    if not os.path.exists(os.path.join(project_dir, "input", image_path)):
        print("Missing input image")
        exit(1)

    if image_path.endswith(".pdf"):
        print("Converting PDF to PNG not implemented yet")
        exit(1)

    elif image_path.endswith(".png"):
        shutil.copyfile(os.path.join(project_dir, "input", image_path), os.path.join(working_dir, "tmp.png"))
        print("Image is already a PNG, skipping conversion.")

    tmp_img_path = os.path.join(working_dir, "tmp.png")
    tmp_cleand_img_path = os.path.join(working_dir, "tmp_cleaned.png")
    img = Image.open(tmp_img_path)
    img.save(tmp_cleand_img_path)
    print("Done: Removing parts of the image")
    del img

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

    if img.width > 2000 or img.height > 2000:
        print(f"Image is larger than 2000x2000 {img.width}x{img.height}")
        c_width = int(img.width / 2)
        c_height = int(img.height / 2)

        while (c_width > 2000 or c_height > 2000):
            print(f"Resizing image to {c_width}x{c_height}")
            file_path = os.path.join(working_dir, f"overlay_{c_width}x{c_height}.png")
            if not os.path.exists(file_path):
                img_part = img.resize((int(c_width), c_height))
                img_part.save(file_path)
                del img_part
            else:
                print(f"Skipped")
            c_width = int(c_width / 2)
            c_height = int(c_height / 2)

    if not os.path.exists(os.path.join(project_dir, "input", "transform.json")):
        print("Missing input config")
        exit(1)

    f = open(os.path.join(project_dir, "input", "transform.json"))
    config = json.loads(f.read())
    f.close()

    imgsize = img.size
    scale_width = imgsize[0] / 945
    scale_height = imgsize[1] / 1335
    del img

    markers_scaled = {}
    for i in range(1,5):
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

    for i in range(1,5):
        print(f"M{i}: {markers_scaled[i]['overlay']['x']}, {markers_scaled[i]['overlay']['y']}")

    logger = logging.getLogger(__name__)
    logger.addHandler(logging.StreamHandler())
    logging.basicConfig(filename=f'{project_dir}/tile.log', level=logging.INFO)
    os.makedirs(os.path.join(working_dir, "generator"), exist_ok=True)
    zoom_max = max(zoom_levels)

    generator = GenerateTiles(
        os.path.join(project_dir, "output"),
        os.path.join(working_dir, "tmp_cleaned.png"),
        markers_scaled,
        zoom=zoom_max,
        logger=logger,
        tmp_dir=os.path.join(working_dir, "generator"),
    )
    generator.run()