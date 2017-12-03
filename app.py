from flask import Flask, request, jsonify, escape
from flask_cors import CORS
from utils.ipfs import IPFSUtils
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
    title = escape(request.form["title"])
    body = escape(request.form["body"])
    thread_id = utils.make_thread(title, body)
    return thread_id


@app.route("/api/get_threads", methods=["GET"])
def get_threads():
    threads_json = utils.get_threads()
    return jsonify(threads_json)


if __name__ == "__main__":
    # Run the server in a H4x0rZ port
    app.run(debug=True, port=1337)
