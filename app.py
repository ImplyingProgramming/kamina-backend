from flask import Flask, request, jsonify, escape
from flask_cors import CORS
from utils.ipfs import IPFSUtils
from utils.images import create_thumbnail
app = Flask(__name__)
CORS(app)
utils = IPFSUtils()


@app.route("/api", methods=["GET"])
def index():
    return "Hi there\n"


@app.route("/api/make_thread", methods=["POST"])
def make_thread():
    """
    We need the title of the thread, the thread body and possibly
    some media, for now just an image
    TODO: add thumbnail functionality
    """
    title = escape(request.json["title"])
    body = escape(request.json["body"])
    # thread_id = utils.make_thread(title, body)
    return "test"


# This should return the ipfs hash of the image and the thumbnail
# TODO: Make thumbnail creation... somehow
@app.route("/api/upload_image", methods=["POST"])
def upload_image():
    image = request.files["file"]
    original_img_hash = utils.upload_image(image)
    thumbnail = create_thumbnail(image)
    thumbnail_hash = utils.upload_image(thumbnail)
    response = {
        "original": original_img_hash,
        "thumbnail": thumbnail_hash
    }
    return jsonify(response)


@app.route("/api/get_threads", methods=["GET"])
def get_threads():
    threads_json = utils.get_threads()
    return jsonify(threads_json)


if __name__ == "__main__":
    # Run the server in a H4x0rZ port
    app.run(debug=True, port=1337)
