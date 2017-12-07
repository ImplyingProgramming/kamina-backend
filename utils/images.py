from PIL import Image
import io


def create_thumbnail(image) -> bytes:
    size = (120, 120)  # Probably increase to a better size
    # This problem happens only when openning .JPG files
    try:
        im = Image.open(image).convert("RGB")
    except IOError:
        im = Image.open(image)
    im.thumbnail(size)
    bytes_img = io.BytesIO()
    im.save(bytes_img, "JPEG")
    return bytes_img.getvalue()
