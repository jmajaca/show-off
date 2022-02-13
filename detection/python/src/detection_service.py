import cv2
import numpy as np
from typing import List

from exceptions import InvalidImageError
from third_party.ctpn_predict import get_det_boxes


class DetectionService:

    @staticmethod
    def read_image_as_string(files: dict) -> str:
        try:
            image = files['image']
            image_string = image.read()
            return image_string
        except Exception as e:
            raise InvalidImageError(e)

    @staticmethod
    def get_text_boxes(image_string: str) -> list:
        np_image = np.fromstring(image_string, np.uint8)
        image = cv2.imdecode(np_image, cv2.IMREAD_COLOR)
        text_boxes = get_det_boxes(image).tolist()
        return sorted(text_boxes, key=lambda box: (min(box[1:-1:2]), min(box[::2])))

    @staticmethod
    def configure_box_response(image_string: str, response_type: str = None) -> List[dict]:
        boxes = DetectionService.get_text_boxes(image_string)
        result = []
        for index, box in enumerate(boxes):
            if response_type == 'minimal':
                points = list(map(int, box[:-1]))
                start_x = min([points[0], points[4]])
                start_y = min([points[1], points[3]])
                end_x = max([points[2], points[6]])
                end_y = max([points[5], points[7]])
                element = {'start_x': start_x, 'start_y': start_y, 'width': end_x - start_x, 'height': end_y - start_y}
            else:
                points = list(map(int, box[:-1]))
                points = [{'axis_x': points[i], 'axis_y': points[i + 1]} for i in range(0, len(points), 2)]
                element = {'ord_num': index, 'points': points, 'probability': round(box[-1], 4)}
            result.append(element)
        return result
