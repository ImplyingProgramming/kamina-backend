from PIL import Image
import ipfsapi
import io
import os, hashlib


class ImagesUtils:
    @staticmethod
    def create_thumbnail(image, size: tuple, post_id: str) -> bytes:
    
        # storage for thumbnail bytes
        bytes_thmb = io.BytesIO() 
        
        # change the size, save it as a png
        thumb_im = Image.open(image)
        thumb_im.thumbnail(size)
        thumb_im.save(bytes_thmb, format="PNG")

        # return raw thumbnail bytes
        return bytes_thmb.getvalue()

    @staticmethod
    def get_image_information(image, img_filename) -> dict:
        information = {
            "size": 0,  # Size in Kilobytes
            "dimensions": None,  # A list [width, height],
            "filename": img_filename
        }
        im = Image.open(image)
        # calculate size of byte buffer in KB
        information["size"] = len(image.read()) / 1024
        # dimensions
        information["dimensions"] = str(im.size[0]) + "x" + str(im.size[1])
        return information
