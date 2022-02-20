from PIL import Image
from werkzeug.datastructures import FileStorage

from ModelWrapper import ModelWrapper


class RecognitionService:

    def __init__(self, model_weights_path: str):
        self.model = ModelWrapper(model_weights_path)

    def get_text_from_image(self, image: FileStorage) -> str:
        return self.model.get_text([Image.open(image)])
