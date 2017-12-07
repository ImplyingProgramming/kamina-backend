import ipfsapi
from ipfsapi.exceptions import StatusError
from .images import ImagesUtils

import json
import io
import random
from datetime import datetime


class IPFSUtils:
    def __init__(self):
        self.ipfs_instance = ipfsapi.connect()
        self.img_utils = ImagesUtils

    @staticmethod
    def get_random_response_id():
        number = ""
        for i in range(8):
            number += str(random.randint(1, 9))
        return number

    def make_thread(self, title, content, image_hashes, image_information, post_id) -> str:
        # We need to make a temporary json file, then add it to ipfs
        ipfs = self.ipfs_instance
        thread_dir = "/threads/" + post_id + "/"
        response_id = self.get_random_response_id()
        thread_data = {
            "title": title,
            "content": content,
            "post_id": post_id,
            "user": "Anonymous",  # For now, until we have user functionality
            "response_id": response_id,
            "image_hashes": image_hashes,
            "image_info": image_information,
            "date_created": datetime.today().timestamp()
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
    def upload_image(self, image, filename, post_id):
        ipfs = self.ipfs_instance
        # Some handy variables
        images_dir = "/images/" + post_id + "/"
        img_location = images_dir + filename
        # Create folder for images
        try:
            ipfs.files_mkdir(images_dir)
        except StatusError as e:
            pass
        # Add the file to the MFS
        ipfs.files_write(img_location, io.BytesIO(image), create=True)
        # Get image information from the MFS
        img_mfs = ipfs.files_stat(img_location)
        return img_mfs["Hash"]

    # Return a list of dictionaries containing the threads information
    # TODO: Return sorted list (new threads, bumped threads, etc...)
    def get_threads(self) -> list:
        ipfs = self.ipfs_instance
        threads_list = []
        threads_ids = ipfs.files_ls("/threads")
        if threads_ids["Entries"] is not None:
            for thread_id in threads_ids["Entries"]:
                thread_mfs_path = "/threads/{}".format(thread_id["Name"])
                thread_info_file = ipfs.files_ls(thread_mfs_path)["Entries"][0]["Name"]
                json_file = json.loads(ipfs.files_read(thread_mfs_path + "/" + thread_info_file))
                threads_list.append(json_file)
        return threads_list
