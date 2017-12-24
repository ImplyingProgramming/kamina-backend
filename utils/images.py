from PIL import Image
import io

class ImagesUtils:
    @staticmethod
    def create_thumbnail(image, size: tuple) -> bytes:
    
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
        im = Image.open(image)
        information = {
            "size": len(image.read()) / 1024,  # Size in Kilobytes
            "dimensions": str(im.size[0]) + "x" + str(im.size[1]),  # A list [width, height],
            "filename": img_filename
        }
        return information
