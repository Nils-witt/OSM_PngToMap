import shutil
from PIL import Image

from celery import shared_task
from api.models import Project
from django.conf import settings
import os
from .tilecalculation.create_marker_overlay import GenerateTiles
from .tilecalculation.tile_calc import resize, create_index_json
@shared_task
def render_project(project_id):
    project = Project.objects.get(id=project_id)
    project.status = 'in_progress'
    project.save()
    try:
        WK_DIR = os.path.join(settings.BASE_DIR, 'render_data', str(project.id))
        if  os.path.exists(WK_DIR):
            shutil.rmtree(WK_DIR)
        os.makedirs(WK_DIR)

        IMG_PATH = os.path.join(WK_DIR, 'input.png')
        TILE_OUTPUT_PATH = os.path.join(WK_DIR, 'tiles')
        TMP_PATH = os.path.join(WK_DIR, 'tmp')
        ZIP_PATH = os.path.join(settings.BASE_DIR, 'rendered_tiles')
        if not os.path.exists(ZIP_PATH):
            os.makedirs(ZIP_PATH)
        if os.path.exists(os.path.join(ZIP_PATH, f'{project.id}.zip')):
            os.remove(os.path.join(ZIP_PATH, f'{project.id}.zip'))
        
        if not os.path.exists(TMP_PATH):
            os.makedirs(TMP_PATH)
        if not os.path.exists(TILE_OUTPUT_PATH):
            os.makedirs(TILE_OUTPUT_PATH)
        pj_img_path = project.image.path

        if pj_img_path.endswith(".png"):
            shutil.copyfile(pj_img_path, IMG_PATH)
            print("Image is already a PNG, skipping conversion.")
        elif pj_img_path.endswith(".jpg"):
            img = Image.open(pj_img_path)
            converted = img.convert("RGBA")
            converted.save(IMG_PATH)

        img = Image.open(IMG_PATH)
        print(f"Image Mode: {img.mode}")

        if img.width > 32766 or img.height > 32766:
            print("Image too large, resizing to 32766")
            if img.width > img.height:
                print("Resizing width")
                wpercent = (32766 / float(img.size[0]))
                hsize = int((float(img.size[1]) * float(wpercent)))
                print(f"Resizing image to {32766}x{hsize}")
                img = img.resize((32766, hsize))
                img.save(IMG_PATH)
            else:
                print("Resizing height")
                hpercent = (32766 / float(img.size[1]))
                wsize = int((float(img.size[0]) * float(hpercent)))
                print(f"Resizing image to {wsize}x{32766}")
                img = img.resize((wsize, 32766))
                img.save(IMG_PATH)

        imgsize = img.size
        print("Ref: Image size: {}".format(imgsize))



        markers_scaled = {}
        if len(project.coordinates) < 4:
            print("Not enough coordinates")
            project.status = 'error'
            project.save()
            return -1
        
        for i in range(0, 4):
            scale_width = imgsize[0] / project.coordinates[i]['img_scale']['width']
            scale_height = imgsize[1] / project.coordinates[i]['img_scale']['height']
            markers_scaled[i] = {
                "overlay": {
                    "x": project.coordinates[i]['img']['x'] * scale_width,
                    "y": project.coordinates[i]['img']['y'] * scale_height
                },
                "map": {
                    "lat": project.coordinates[i]['map']['latitude'],
                    "lng": project.coordinates[i]['map']['longitude']
                }
            }
        del img
        print("Markers on input image:")
        for i in range(0, 4):
            print(f"M{i}: {markers_scaled[i]['overlay']['x']}, {markers_scaled[i]['overlay']['y']}")

        print(f"Max zoom level: {project.max_zoom}")

        print("STEP 5: Run Generator")

        generator = GenerateTiles(
            TILE_OUTPUT_PATH,
            IMG_PATH,
            markers_scaled,
            zoom=project.max_zoom,
            tmp_dir=TMP_PATH,
        )
        generator.run()


        for i in range(project.max_zoom - 1, project.min_zoom - 1, -1):
            print(f"Resizing zoom level to {i}...")
            resize(TILE_OUTPUT_PATH, i)
            print(f"Done for zoom level {i}.")
        create_index_json(TILE_OUTPUT_PATH)
        shutil.make_archive(os.path.join(WK_DIR, 'tiles'), 'zip', TILE_OUTPUT_PATH)
        shutil.move(os.path.join(WK_DIR, 'tiles.zip'), os.path.join(ZIP_PATH, f'{project.id}.zip'))

        shutil.rmtree(WK_DIR)
        project.status = 'completed'
        project.save()
    except Exception as e:
        print(f"Error during rendering: {e}")
        project.status = 'error'
        project.save()
    return project.status