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


@app.route("/api/upload_image", methods=["POST"])
def upload_image():
    image_file = request.files["file"]
    # Original image data
    image_extension = image_file.filename.split(".")[-1]
    image_basename = ".".join(image_file.filename.split(".")[0:-1])
    image_filename = image_basename + "." + image_extension
    image_ipfs_hash = utils.upload_image(image_file.read(), image_filename)
    # Thumbnail data
    thumbnail_file = create_thumbnail(image_file)
    thumbnail_filename = image_basename + "-thumbnail.jpeg"
    thumbnail_ipfs_hash = utils.upload_image(thumbnail_file, thumbnail_filename)
    # thumbnail_ipfs_hash = "test"
    response = {
        "original": image_ipfs_hash,
        "thumbnail": thumbnail_ipfs_hash
    }
    return jsonify(response)


@app.route("/api/get_threads", methods=["GET"])
def get_threads():
    threads_json = utils.get_threads()
    return jsonify(threads_json)


if __name__ == "__main__":
    # Run the server in a H4x0rZ port
    app.run(debug=True, port=1337)
