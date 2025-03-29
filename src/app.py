import json
import logging
import os
import shutil
import threading

from flask import Flask, send_file, request, redirect, Response

from create_marker_overlay import GenerateTiles

os.makedirs("tmp", exist_ok=True)

application = Flask(__name__)


@application.route("/")
def main():
    return send_file("static/index.html")


@application.route("/map")
def map():
    return send_file("static/map.html")


@application.route("/overlayPicture", methods=["GET", "POST"])
def overlay_picture():
    if request.method == "GET":
        if not os.path.isfile("tmp/overlayPicture.png"):
            return "No overlay picture"
        return send_file("tmp/overlayPicture.png")
    if request.method == "POST":
        f = request.files['overlayPicture']
        f.save("tmp/overlayPicture.png")
        return redirect('/')


@application.route("/config", methods=["GET", "POST"])
def config():
    if request.method == 'POST':
        data = request.json
        with open("tmp/config.json", "w") as f:
            f.write(json.dumps(data))
        return "ok"
    if request.method == 'GET':
        return send_file("tmp/config.json")


@application.route("/tiles", methods=["GET"])
def tiles():
    dirs = [f for f in os.listdir("tmp/tiles") if os.path.isdir(os.path.join("tmp/tiles", f))]
    data = {}
    for d in dirs:
        data[d] = {}
        for x in os.listdir(os.path.join("tmp/tiles", d)):
            data[d][x] = os.listdir(os.path.join("tmp/tiles", d, x))
    return json.dumps(data)


@application.route("/tiles/<int:z>/<int:x>/<int:y>", methods=["GET"])
def tile(z, x, y):
    if os.path.isfile(f"tmp/tiles/{z}/{x}/{y}.png"):
        return send_file(f"tmp/tiles/{z}/{x}/{y}.png")
    return Response("{'status':'Not found'}", status=404, mimetype='application/json')


def tilegen_thread():
    if os.path.isfile(f"tmp/tile.log"):
        os.remove("tmp/tile.log")
    logger = logging.getLogger(__name__)
    logger.addHandler(logging.StreamHandler())
    logging.basicConfig(filename='tmp/tile.log', level=logging.INFO)

    with open('tmp/config.json') as json_data:
        d = json.loads(json_data.read())
        json_data.close()
        zooms = range(d['minZoom'], d['maxZoom'] + 1)
        for zoom in zooms:
            print("Generating tiles for zoom", zoom)
            generator = GenerateTiles("tmp/tiles", 'tmp/overlayPicture.png', zoom=zoom, logger=logger)
            generator.run()


@application.route("/generate_tiles", methods=["GET"])
def generate_tiles():
    threading.Thread(target=tilegen_thread, ).start()
    return redirect("/")


@application.route("/tilelog", methods=["GET"])
def tile_log():
    if os.path.isfile(f"tmp/tile.log"):
        return send_file(f"tmp/tile.log")
    return "No log file"


@application.route("/download_tiles", methods=["GET"])
def download_tiles():
    shutil.make_archive("tmp/tiles_zip", 'zip', "tmp/tiles/")
    return send_file("tmp/tiles_zip.zip")
