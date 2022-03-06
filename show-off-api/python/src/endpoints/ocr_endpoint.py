import io
import logging
import uuid
from datetime import datetime

import cv2
from flask import Blueprint, request
from flask_cors import cross_origin

import env
from api.api import DetectionAPI, RecognitionAPI
from exceptions.exceptions import ImageDimensionsTooLargeError
from services.image_service import ImageService
from services.queue_service import QueueService

ocr_endpoint = Blueprint('ocr_endpoint', __name__)

detection_api = DetectionAPI()
recognition_api = RecognitionAPI()

queue_service = QueueService()


@ocr_endpoint.route('/read', methods=['POST'])
@cross_origin()
def read_image():
    """Endpoint for submitting image with text so that text can be extracted
    ---
    post:
      description: Submit image with text
      responses:
        200:
          description: Text is successfully extracted
          content:
            application/json:
              schema:
                type: string
                example: TODO
        400:
          description: Image is not acceptable
    """
    request_id = uuid.uuid4().__str__()
    files = request.files.to_dict()
    image = files['image']
    cv2_image = ImageService.cv2_convert(image)
    try:
        ImageService.check_dimensions(cv2_image)
    except ImageDimensionsTooLargeError as e:
        logging.error('Invalid image', e)
        return {'timestamp': datetime.now(), 'error': str(e)}, 400
    queue_service.send_image(request_id, image)
    text_boxes = detection_api.get_minimal_text_boxes(image)
    images = []
    for i, box in enumerate(text_boxes):
        cut_image = ImageService.cut_min_box(cv2_image, box)
        # cv2.imwrite(f'{i}.jpg', cut_image)
        is_success, buffer = cv2.imencode('.jpg', cut_image)
        images.append(io.BytesIO(buffer))
    extracted_text = recognition_api.extract_text(images)
    text = ' '.join(extracted_text.tokens)
    queue_service.send_image_data(request_id, text_boxes, text)
    return {'id': request_id, 'text': text}, 200


@ocr_endpoint.route('/correct-text', methods=['POST'])
@cross_origin()
def correct_text():
    return '', 404
