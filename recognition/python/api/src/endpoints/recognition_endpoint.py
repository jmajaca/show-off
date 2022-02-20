from flask import Blueprint, request
from werkzeug.datastructures import FileStorage

import api_env
from recognition_service import RecognitionService

recognition_endpoint = Blueprint('recognition_endpoint', __name__)

recognition_service = RecognitionService(api_env.model_weights_path)


@recognition_endpoint.route('/extract', methods=['POST'])
def extract():
    """Endpoint for extracting text from images
    ---
    post:
      description: Extracted text from images
      responses:
        200:
          description: Text was successfully extracted from images
    """
    files: dict[str, FileStorage] = request.files.to_dict()
    keys: list[str] = sorted([key for key in files.keys()])
    images: list[FileStorage] = [files[key] for key in keys]
    for key in keys:
        if not key.startswith('image'):
            # log warning
            print('Invalid key:', key)
            raise Exception()
    return {'tokens': recognition_service.get_text_from_images(images)}, 200
