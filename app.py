from flask import Flask, request, jsonify, escape
from flask_cors import CORS
from utils.ipfs import IPFSUtils
from utils.images import ImagesUtils


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
        routes = [{"r": "/api",              "m": ["GET"],  "f": self.index},
                  {"r": "/api/",             "m": ["GET"],  "f": self.index},
                  {"r": "/api/make_thread",  "m": ["POST"], "f": self.make_thread},
                  {"r": "/api/upload_image", "m": ["POST"], "f": self.upload_image},
                  {"r": "/api/get_threads",  "m": ["GET"],  "f": self.get_threads},
                  {"r": "/api/get_thread",   "m": ["POST"],  "f": self.get_thread},
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
        image_extension = image_filename.split(".")[-1]
        image_format = image_file.mimetype.split("/")[-1]
        image_basename = image_filename[:-(len(image_extension) + 1)]  # Plus the dot (.)
        image_ipfs_hash = self.ipfs_utils.upload_image(image_file.read(), image_filename, post_id)
        # Thumbnail data
        thumbnail_file = self.img_utils.create_thumbnail(image_file, image_format, (240, 240))
        thumbnail_filename = image_basename + "-thumbnail.jpg"
        thumbnail_ipfs_hash = self.ipfs_utils.upload_image(thumbnail_file, thumbnail_filename, post_id)
        image_information = self.img_utils.get_image_information(image_file, image_format, image_filename)
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
        if "post_id" not in request.json.keys():
            # 400 bad request
            return jsonify({"err": "Post ID not provided in request"}), 400

        thread_id = escape(request.json["post_id"])
        try:
            # Return json of threads
            return jsonify(self.ipfs_utils.get_thread(thread_id))
        except FileNotFoundError as err:
            # Thread doesn't exist
            # 404 not found
            return jsonify({"err": "Thread with post id '" + thread_id + "' does not exist"}), 404


if __name__ == "__main__":
    # Run the server in a H4x0rZ port
    API().app.run(debug=True, port=1337)
