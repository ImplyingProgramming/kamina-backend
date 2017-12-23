from flask import Flask, request, jsonify, escape
from flask_cors import CORS
from utils.ipfs import IPFSUtils
from utils.images import ImagesUtils
from os.path import basename


class API:
    """
    Base class for Kamina's backend.
    """
    app = Flask(__name__)
    CORS(app)
    ipfs_utils = IPFSUtils()
    img_utils = ImagesUtils()

    def __init__(self):
        # Routes
        routes = [
            {"r": "/api",              "m": ["GET"],  "f": self.index},
            {"r": "/api/",             "m": ["GET"],  "f": self.index},
            {"r": "/api/make_thread",  "m": ["POST"], "f": self.make_thread},
            {"r": "/api/upload_image", "m": ["POST"], "f": self.upload_image},
            {"r": "/api/get_threads",  "m": ["GET"],  "f": self.get_threads},
            {"r": "/api/get_thread",   "m": ["GET"],  "f": self.get_thread},
        ]

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
        # FIXME I don't think flask.escape() is used for this, I think this would be escaping it twice
        # I though flask.escape() was for escaping HTML, not JSON queries?
        title = escape(request.json["thread_title"])
        content = escape(request.json["thread_content"])
        post_id = request.json["post_id"]
        try:
            image_hashes = request.json["thread_image_hashes"]
            image_info = request.json["thread_image_info"]
        except KeyError:
            image_hashes = {}
            image_info = {}
        response_id = self.ipfs_utils.make_thread(title, content, image_hashes, image_info, post_id)
        return response_id

    def upload_image(self):
        # Check if the user added an image
        if not request.files.getlist("file"):
            return jsonify({})

        image_file = request.files["file"]
        post_id = request.form["post_id"]

        # Original image data
        image_filename = image_file.filename
        image_ipfs_hash = self.ipfs_utils.upload_image(image_file.read(), image_filename, post_id)
        image_information = self.img_utils.get_image_information(image_file, image_filename)

        # Thumbnail data
        thumbnail_file = self.img_utils.create_thumbnail(image_file, (240, 240), post_id)
        thumbnail_filename = basename(image_filename) + "-thumbnail.png"
        thumbnail_ipfs_hash = self.ipfs_utils.upload_image(thumbnail_file, thumbnail_filename, post_id)

        response = [
            image_information,
            {
                "original": image_ipfs_hash,
                "thumbnail": thumbnail_ipfs_hash
            }
        ]
        return jsonify(response)

    def get_threads(self):
        threads_json = self.ipfs_utils.get_threads()
        return jsonify(threads_json)

    def get_thread(self):
        # Invalid request
        if "post-id" not in request.values.keys():
            # 400 bad request
            return jsonify({"err": "Post ID not provided in request"}), 400
        thread_id = request.values["post-id"]
        # Empty post ID
        if not thread_id:
            return jsonify({"err": "Thread with post id '{}' does not exist".format(thread_id)}), 404
        thread_json = self.ipfs_utils.get_thread(thread_id)
        # If there is an error, return response code
        if "err" in thread_json.keys():
            return jsonify(thread_json), 404
        return jsonify(thread_json)


if __name__ == "__main__":
    # Run the server in a H4x0rZ port
    API().app.run(debug=True, port=1337)
