from PIL import Image

import io
import os


class ImagesUtils:
    @staticmethod
    def create_thumbnail(image, img_format) -> bytes:
        size = (120, 120)  # Probably increase to a better size
        # This problem happens only when openning .JPG files
        try:
            im = Image.open(image).convert("RGB")
        except IOError:
            im = Image.open(image)
        im.thumbnail(size)
        bytes_img = io.BytesIO()
        im.save(bytes_img, img_format)
        return bytes_img.getvalue()

    @staticmethod
    def get_image_information(image, img_format, img_filename) -> dict:
        information = {
            "size": 0,  # Size in Kilobytes
            "dimensions": None,  # A list [width, height],
            "filename": img_filename
        }
        try:
            im = Image.open(image).convert("RGB")
        except IOError:
            im = Image.open(image)
        img_bytes = io.BytesIO()
        im.save(img_bytes, img_format)
        img_bytes.seek(0, os.SEEK_END)
        information["size"] = img_bytes.tell() / 1024
        information["dimensions"] = str(im.size[0]) + "x" + str(im.size[1])
        return information
