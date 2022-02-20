from abc import ABC
from enum import Enum

import requests
from requests import Response
from werkzeug.datastructures import FileStorage

import env
from models.detection_api import TextBox, MinimalTextBox
from models.recognition_api import RecognitionResponse


class PayloadType(Enum):
    JSON = 'json'
    FILE = 'file'


class API(ABC):

    def __init__(self, base_url: str):
        self.base_url = base_url

    def get(self, path: str) -> Response:
        return requests.get(url=self.base_url + path)

    def post(self, path: str, payload: dict, content_type: PayloadType) -> Response:
        if content_type == PayloadType.JSON:
            return requests.post(url=self.base_url + path, json=payload)
        elif content_type == PayloadType.FILE:
            return requests.post(url=self.base_url + path, files=payload)


class DetectionAPI(API):

    def __init__(self):
        super().__init__(env.DETECTION_API_URL)

    def get_text_boxes(self, image: FileStorage) -> list[TextBox]:
        response = self.post(path='/boxes', payload={'image': image}, content_type=PayloadType.FILE)
        return [TextBox(**element) for element in response.json()]

    def get_minimal_text_boxes(self, image: FileStorage) -> list[MinimalTextBox]:
        response = self.post(path='/minimal-boxes', payload={'image': image}, content_type=PayloadType.FILE)
        return [MinimalTextBox(**element) for element in response.json()]


class RecognitionAPI(API):

    def __init__(self):
        super().__init__(env.RECOGNITION_API_URL)

    def extract_text(self, images: list) -> RecognitionResponse:
        payload = {f'image{i}': image for i, image in enumerate(images)}
        response = self.post(path='/extract', payload=payload, content_type=PayloadType.FILE)
        return RecognitionResponse(**response.json())
