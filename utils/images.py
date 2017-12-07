from PIL import Image
import io


def create_thumbnail(image) -> bytes:
    size = (120, 120)
    try:
        im = Image.open(image).convert("RGB")
    except IOError:
        im = Image.open(image)
    im.thumbnail(size)
    bytes_img = io.BytesIO()
    im.save(bytes_img, "JPEG")
    return bytes_img.getvalue()
