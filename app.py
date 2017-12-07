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
    """
    # Thread information from request
    title = escape(request.json["thread_title"])
    body = escape(request.json["thread_content"])
    post_id = request.json["post_id"]
    image = request.json["thread_image_hashes"]
    response_id = utils.make_thread(title, body, image, post_id)
    return response_id


@app.route("/api/upload_image", methods=["POST"])
def upload_image():
    image_file = request.files["file"]
    post_id = request.form["post_id"]
    # Original image data
    image_extension = image_file.filename.split(".")[-1]
    image_basename = ".".join(image_file.filename.split(".")[0:-1])
    image_filename = image_basename + "." + image_extension
    image_ipfs_hash = utils.upload_image(image_file.read(), image_filename, post_id)
    # Thumbnail data
    thumbnail_file = create_thumbnail(image_file)
    thumbnail_filename = image_basename + "-thumbnail.jpeg"
    thumbnail_ipfs_hash = utils.upload_image(thumbnail_file, thumbnail_filename, post_id)
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
