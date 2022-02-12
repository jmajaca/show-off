import cv2
import numpy as np

from third_party.ctpn_predict import get_det_boxes


class Detection:

    @staticmethod
    def get_text_boxes(image_string: str) -> list:
        np_image = np.fromstring(image_string, np.uint8)
        image = cv2.imdecode(np_image, cv2.IMREAD_COLOR)
        text_boxes = get_det_boxes(image).tolist()
        return sorted(text_boxes, key=lambda box: (min(box[1:-1:2]), min(box[::2])))
