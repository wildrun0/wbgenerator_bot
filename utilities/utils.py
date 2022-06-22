from ast import Bytes
from os import stat
import random
import string
from io import BytesIO


class Utils():
    @staticmethod
    def uuid_gen(length: int = 8) -> str:
        return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(length))

    @staticmethod
    def image2file_bytes(image) -> BytesIO:
        """Return `image` as PNG file-like object."""
        image_file = BytesIO()
        image.save(image_file, format="PNG")
        return image_file