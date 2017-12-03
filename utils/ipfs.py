import ipfsapi
import os
import json
import uuid
import io
import datetime


class IPFSUtils:
    def __init__(self):
        self.ipfs_instance = ipfsapi.connect()

    def make_thread(self, title, body) -> str:
        # TODO: Make add images to ipfs functionality
        # We need to make a temporary json file, then add it to ipfs
        ipfs = self.ipfs_instance
        thread_id = str(uuid.uuid4())
        working_dir = os.path.dirname(os.path.realpath(__file__))
        json_file = working_dir + "/tmp/info.json"
        thread_dir = "/threads/" + thread_id + "/"
        thread_data = {
            "title": title,
            "body": body,
            "id": thread_id
        }
        with open(json_file, "w+") as f:
            json.dump(thread_data, f, indent=4)
        # Add file to ipfs
        ipfs.add(json_file)
        # Create a file for the thread in the file system
        ipfs.files_mkdir(thread_dir)
        # Now add it to the /threads directory in ipfs
        with open(json_file, "rb") as f:
            ipfs.files_write(thread_dir + "info.json", io.BytesIO(f.read()), create=True)
        # Now delete file
        os.remove(json_file)
        return thread_id

    # Return a list of dictionaries containing the threads information
    # TODO: Return sorted list (new threads, bumped threads, etc...)
    def get_threads(self) -> list:
        ipfs = self.ipfs_instance
        threads_list = []
        threads_ids = ipfs.files_ls("/threads")
        for thread_id in threads_ids["Entries"]:
            thread_mfs_path = "/threads/{}".format(thread_id["Name"])
            thread_info_file = ipfs.files_ls(thread_mfs_path)["Entries"][0]["Name"]
            json_file = json.loads(ipfs.files_read(thread_mfs_path + "/" + thread_info_file))
            threads_list.append(json_file)
        return threads_list
