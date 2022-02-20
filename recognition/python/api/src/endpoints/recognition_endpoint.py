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
    texts: list[str] = []
    keys: list[str] = sorted([key for key in files.keys()])
    for key in keys:
        if not key.startswith('image'):
            # log warning
            print('Invalid key:', key)
            continue
        texts.append(recognition_service.get_text_from_image(files[key]))
    return {'tokens': texts}, 200
