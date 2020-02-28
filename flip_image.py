from mitmproxy import http
from PIL import Image
import io

ignore_type = ('gif', 'x-icon')


def image_from_memory(img: bytes) -> Image:
    """new Image from in-memory image file"""
    return Image.open(io.BytesIO(img))


def image_to_bytes(img: Image, img_type: str) -> bytes:
    temp = io.BytesIO()
    img.save(temp, format=img_type)
    return temp.getvalue()


def response(flow: http.HTTPFlow) -> None:
    """Turn all images upside down"""
    # headers is a dict
    content_type = flow.response.headers.get('content-type', '')
    if content_type.startswith('image'):
        img_type = content_type.split('/')[1]
        if img_type in ignore_type:
            return

        im = image_from_memory(flow.response.content)

        # this will make the image hard to read
        # im_flipped = im.transpose(method=Image.FLIP_TOP_BOTTOM)

        im_flipped = im.rotate(180)
        flow.response.content = image_to_bytes(im_flipped, img_type)
