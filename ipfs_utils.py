import ipfsapi
import os
import json
import uuid
import io


class IPFSUtils:
    def __init__(self):
        self.ipfs_instance = ipfsapi.connect()

    def make_thread(self, title, body):
        # We need to make a temporary file, then add it to ipfs
        # use json for this
        ipfs = self.ipfs_instance
        thread_id = str(uuid.uuid4()).split("-")[0]
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
        # Create a file for the thread in the MFS
        ipfs.files_mkdir(thread_dir)
        # Now add it to the /threads directory in ipfs
        with open(json_file, "rb") as f:
            ipfs.files_write(thread_dir + "info.json", io.BytesIO(f.read()), create=True)
        # Now delete file
        os.remove(json_file)
