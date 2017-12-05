import ipfsapi
import json
import uuid
import io


class IPFSUtils:
    def __init__(self):
        self.ipfs_instance = ipfsapi.connect()

    def make_thread(self, title, body) -> str:
        # TODO: Make add images to ipfs functionality
        # We need to make a temporary json file, then add it to ipfs
        ipfs = self.ipfs_instance
        thread_id = str(uuid.uuid4())  # Maybe we could use other ways of identifying threads
        thread_dir = "/threads/" + thread_id + "/"
        thread_data = {
            "title": title,
            "body": body,
            "id": thread_id
        }
        # Dump the thread_data list to a string for thread uploading to ipfs
        json_str = json.dumps(thread_data, indent=4)
        # Create a directory for the thread in the MFS
        ipfs.files_mkdir(thread_dir)
        # Now add the thread information as a file info.json to the thread_dir
        ipfs.files_write(thread_dir + "info.json", io.BytesIO(str.encode(json_str)), create=True)
        return thread_id

    # TODO: Check for only images (mimetype)
    # We suppose we have a directory in the MFS called /images
    def upload_image(self, image):
        ipfs = self.ipfs_instance
        # Some hand variables
        images_dir = "/images/"
        filename = image.filename
        img_location = images_dir + filename
        # Add the file to the MFS
        ipfs.files_write(img_location, io.BytesIO(image.stream.read()), create=True)
        # Get image information from the MFS
        img_mfs = ipfs.files_stat(img_location)
        return img_mfs["Hash"]

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
