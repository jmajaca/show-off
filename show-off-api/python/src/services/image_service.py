import cv2
import numpy as np
from werkzeug.datastructures import FileStorage

from exceptions.exceptions import ImageDimensionsTooLargeError
from models.detection_api import TextBox, MinimalTextBox


class ImageService:

    @staticmethod
    def cv2_convert(image: FileStorage) -> np.ndarray:
        image_string = image.read()
        image.stream.seek(0)
        np_image = np.fromstring(image_string, np.uint8)
        return cv2.imdecode(np_image, cv2.IMREAD_COLOR)

    @staticmethod
    def check_dimensions(image: np.ndarray):
        height, width, channels = image.shape
        if height >= 1000 or width >= 1000:
            raise ImageDimensionsTooLargeError(1000, height, 1000, width)

    @staticmethod
    def cut_box(image: np.ndarray, box: TextBox) -> np.ndarray:
        start_y, start_x = box.points[0].axis_y, box.points[0].axis_x
        height = box.points[2].axis_y - start_y
        width = box.points[1].axis_x - start_x
        crop_img = image[start_y:start_y + height, start_x:start_x + width].copy()
        return crop_img

    @staticmethod
    def cut_min_box(image: np.ndarray, box: MinimalTextBox) -> np.ndarray:
        crop_img = image[box.start_y:box.start_y + box.height, box.start_x:box.start_x + box.width].copy()
        return crop_img
