from PIL import Image
import numpy as np


def load_image(uploaded_file) -> Image.Image:
    image = Image.open(uploaded_file)
    return image.convert("RGB")


def image_to_bytes(image: Image.Image) -> bytes:
    return image.tobytes()


def bytes_to_image(data: bytes, size: tuple[int, int]) -> Image.Image:
    width, height = size
    required_length = width * height * 3

    data = data[:required_length]

    if len(data) < required_length:
        data += bytes(required_length - len(data))

    array = np.frombuffer(data, dtype=np.uint8)
    array = array.reshape((height, width, 3))

    return Image.fromarray(array, "RGB")