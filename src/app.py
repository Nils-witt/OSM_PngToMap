import json
import os

from flask import Flask, send_file, request, redirect

os.makedirs("tmp", exist_ok=True)

application = Flask(__name__)


@application.route("/")
def main():
    return send_file("static/index.html")


@application.route("/overlayPicture", methods=["GET", "POST"])
def overlay_picture():
    if request.method == "GET":
        return send_file("tmp/overlayPicture.png")

    if request.method == "POST":
        f = request.files['overlayPicture']
        f.save("tmp/overlayPicture.png")
        return redirect('/')


@application.route("/markers", methods=["GET", "POST"])
def markers():
    if request.method == 'POST':
        data = request.json
        with open("tmp/markers.json", "w") as f:
            f.write(json.dumps(data))
        return "ok"
    if request.method == 'GET':
        return send_file("tmp/markers.json")
