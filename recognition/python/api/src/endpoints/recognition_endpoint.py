import logging
from datetime import datetime

from flask import Blueprint, request
from werkzeug.datastructures import FileStorage

import env_api
from recognition_schema import *
from recognition_service import RecognitionService

recognition_endpoint = Blueprint('recognition_endpoint', __name__)

recognition_service = RecognitionService(env_api.model_weights_path)

log = logging.getLogger(__name__)


@recognition_endpoint.route('/extract', methods=['POST'])
def extract():
    """Endpoint for extracting text from images
    ---
    post:
      description: Extracted text from images
      requestBody:
        content:
          multipart/form-data:
            schema: ExtractRequestSchema
      responses:
        200:
          description: Text was successfully extracted from images
          content:
            application/json:
              schema: ExtractResponseSchema
        400:
          description: Invalid request sent
          content:
            application/json:
              schema: ErrorSchema
        500:
          description: All other errors
    """
    files: dict[str, FileStorage] = request.files.to_dict()
    keys: list[str] = sorted([key for key in files.keys()])
    images: list[FileStorage] = [files[key] for key in keys]
    for key in keys:
        if not key.startswith('image'):
            log.warning(f'Received invalid key {key}')
            return {'timestamp': datetime.now(), 'error': f'Key "{key}" is invalid'}, 400
    return {'tokens': recognition_service.get_text_from_images(images)}, 200
