from flask import Flask, request, jsonify, escape
from flask_cors import CORS
from utils.ipfs import IPFSUtils
from utils.images import create_thumbnail


class API:
    """
    Base class for Kamina's backend.
    """
    app = Flask(__name__)
    CORS(app)
    utils = IPFSUtils()

    def __init__(self):
        # Routes
        routes = [{"r": "/api",              "m": ["GET"],  "f": self.index},
                  {"r": "/api/",             "m": ["GET"],  "f": self.index},
                  {"r": "/api/make_thread",  "m": ["POST"], "f": self.make_thread},
                  {"r": "/api/upload_image", "m": ["POST"], "f": self.upload_image},
                  {"r": "/api/get_threads",  "m": ["GET"],  "f": self.get_threads}, ]

        for route in routes:
            self.add_route(route)

    def add_route(self, route):
        self.app.add_url_rule(route["r"], view_func=route["f"], methods=route["m"])

    @staticmethod
    def index():
        return "Hi there\n"

    def make_thread(self):
        """
        We need the title of the thread, the thread body and possibly
        some media, for now just an image
        """
        # Thread information from request
        title = escape(request.json["thread_title"])
        body = escape(request.json["thread_content"])
        post_id = request.json["post_id"]
        image = request.json["thread_image_hashes"]
        response_id = self.utils.make_thread(title, body, image, post_id)
        return response_id

    def upload_image(self):
        image_file = request.files["file"]
        post_id = request.form["post_id"]
        # Original image data
        image_extension = image_file.filename.split(".")[-1]
        image_basename = ".".join(image_file.filename.split(".")[0:-1])
        image_filename = image_basename + "." + image_extension
        image_ipfs_hash = self.utils.upload_image(image_file.read(), image_filename, post_id)
        # Thumbnail data
        thumbnail_file = create_thumbnail(image_file)
        thumbnail_filename = image_basename + "-thumbnail.jpeg"
        thumbnail_ipfs_hash = self.utils.upload_image(thumbnail_file, thumbnail_filename, post_id)
        # thumbnail_ipfs_hash = "test"
        response = {
            "original": image_ipfs_hash,
            "thumbnail": thumbnail_ipfs_hash
        }
        return jsonify(response)

    def get_threads(self):
        threads_json = self.utils.get_threads()
        return jsonify(threads_json)


if __name__ == "__main__":
    # Run the server in a H4x0rZ port
    API().app.run(debug=True, port=1337)
