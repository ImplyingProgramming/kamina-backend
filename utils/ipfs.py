import ipfsapi
from ipfsapi.exceptions import StatusError
from ipfsapi.exceptions import ErrorResponse
from .images import ImagesUtils

import json
import io
import random
from datetime import datetime


class IPFSUtils:
    ipfs_instance = ipfsapi.connect()
    img_utils = ImagesUtils

    def __init__(self):
        ipfs = self.ipfs_instance
        # Create needed folders inside the MFS
        try:
            ipfs.files_mkdir("/threads")
            ipfs.files_mkdir("/images")
        except StatusError:
            # We get an error if the files already exist
            pass

    @staticmethod
    def get_random_response_id() -> str:
        number = ""
        for i in range(8):
            number += str(random.randint(1, 9))
        return number

    def make_thread(self, user_input: dict) -> str:
        # We need to make a temporary json file, then add it to ipfs
        ipfs = self.ipfs_instance
        thread_dir = "/threads/" + user_input["post_id"] + "/"
        response_id = self.get_random_response_id()
        thread_data = {
            "title": user_input["title"],
            "content": user_input["content"],
            "post-id": user_input["post_id"],
            "user": user_input["username"],
            "response-id": response_id,
            "image-hashes": user_input["image_hashes"],
            "image-info": user_input["image_info"],
            "date-created": datetime.today().timestamp()
        }
        # Dump the thread_data list to a string for thread uploading to ipfs
        json_str = json.dumps(thread_data, indent=4)
        # Create a directory for the thread in the MFS
        ipfs.files_mkdir(thread_dir)
        # Now add the thread information as a file info.json to the thread_dir
        ipfs.files_write(thread_dir + "info.json", io.BytesIO(str.encode(json_str)), create=True)
        return response_id

    # TODO: Check for only images (mimetype)
    # We suppose we have a directory in the MFS called /images
    # The image should be a File like object
    def upload_image(self, image, filename, post_id) -> str:
        ipfs = self.ipfs_instance
        # Some handy variables
        images_dir = "/images/" + post_id + "/"
        # Create folder for image
        try:
            ipfs.files_mkdir(images_dir)
        except StatusError:
            pass
        img_location = images_dir + filename
        # Add the file to the MFS
        ipfs.files_write(img_location, io.BytesIO(image), create=True)
        # Get image information from the MFS
        img_mfs = ipfs.files_stat(img_location)
        return img_mfs["Hash"]

    # Return a list of dictionaries containing the threads information
    def get_threads(self) -> list:
        ipfs = self.ipfs_instance
        threads_list = []
        # We get a dictionary with a single key (Entries) which contains a list of all the IDs
        threads_ids = ipfs.files_ls("/threads")["Entries"]
        if threads_ids is None:
            return threads_list
        # Loop through the list
        for thread_id in threads_ids:
            # make a path in the form /threads/some_uuid4
            thread_mfs_path = "/threads/{}".format(thread_id["Name"])
            # We then again get a dictionary with a single key (Entries), access its content directly
            thread_info_file = ipfs.files_ls(thread_mfs_path)["Entries"][0]["Name"]
            # create a dictionary from a json-formatted (((string)))
            json_file = json.loads(ipfs.files_read(thread_mfs_path + "/" + thread_info_file).decode("utf-8"))
            # append the new created dictionary
            threads_list.append(json_file)
        # Now sort the dictionary according to their creation date
        # TODO: Make bumping functionality (somehow)
        # Get all timestamps (There is probably a better way than doing this)
        timestamps = []
        sorted_thread_list = []
        # Get a list of all the thread's timestamps
        for thread in threads_list:
            timestamps.append(thread["date-created"])
        # Sort the timestamps in reverse
        sorted_timestamps = sorted(timestamps, reverse=True)
        for timestamp in sorted_timestamps:
            for thread in threads_list:
                # Check if the current thread has same timestamp, if so, push it
                if thread["date-created"] == timestamp:
                    sorted_thread_list.append(thread)
        return sorted_thread_list

    def get_thread(self, post_id) -> dict:
        ipfs = self.ipfs_instance
        thread_dir = "/threads/" + post_id + "/"

        # raises ipfsapi.exceptions.ErrorResponse if file doesn't exist
        try:
            thread_info_file = ipfs.files_ls(thread_dir)["Entries"][0]["Name"]
            json_file = json.loads(ipfs.files_read(thread_dir + "/" + thread_info_file).decode("utf-8"))
        except ErrorResponse:
            # Thread doesn't exist
            json_file = {"err": "Thread with post_id '{}' does not exist".format(post_id)}

        return json_file
