from abc import ABC
from enum import Enum

import requests
from requests import Response
from werkzeug.datastructures import FileStorage

from src import env
from src.models.detection_api import TextBox


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
        return response.json()
