from PIL import Image

import io
import os


class ImagesUtils:
    @staticmethod
    def create_thumbnail(image, img_format: str, size: tuple) -> bytes:
        # This problem happens only when openning .JPG files
        try:
            im = Image.open(image).convert("RGB")
        except IOError:
            im = Image.open(image)
        bytes_img = io.BytesIO()
        # Saves image bytes into bytes_img buffer
        # Use PNG as default thumbnail type, REQUIRED to preserve transparency
        if im.format == "GIF":
            # FIXME: PIL works poorly with transperant gifs. fix this at a later date
            # Gather palette info of first frame of GIF
            im.putpalette(im.getpalette())
            # Create a new image with this palette, save it as PNG
            new_im = Image.new("RGBA", im.size)
            new_im.paste(im)
            new_im.thumbnail(size)
            new_im.save(bytes_img, format="PNG")
        else:
            im.thumbnail(size)
            # TODO: Replace img_format with im.format ? What if a file has no extension?
            im.save(bytes_img, format="PNG")

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
