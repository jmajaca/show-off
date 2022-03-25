import io
import logging
import uuid
from datetime import datetime

import cv2
from flask import Blueprint, request
from flask_cors import cross_origin

from api.api import DetectionAPI, RecognitionAPI
from services.image_service import ImageService
from services.queue_service import QueueService

ocr_endpoint = Blueprint('ocr_endpoint', __name__)

log = logging.getLogger(__name__)

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
    try:
        image = files['image']
        cv2_image = ImageService.cv2_convert(image)
        ImageService.check_dimensions(cv2_image)
    except Exception as e:
        log.error('Invalid image', exc_info=True)
        return {'timestamp': datetime.now(), 'error': str(e)}, 400
    queue_service.send_image(request_id, image)
    text_boxes = detection_api.get_minimal_text_boxes(image)
    images = []
    for i, box in enumerate(text_boxes):
        cut_image = ImageService.cut_min_box(cv2_image, box)
        is_success, buffer = cv2.imencode('.jpg', cut_image)
        images.append(io.BytesIO(buffer))
    if len(text_boxes) != 0:
        extracted_text = recognition_api.extract_text(images).tokens
        text = ' '.join(extracted_text)
    else:
        extracted_text = []
        text = ''
    queue_service.send_image_data(request_id, text_boxes, extracted_text)
    return {'id': request_id, 'text': text}, 200


@ocr_endpoint.route('/correct-text', methods=['POST'])
@cross_origin()
def correct_text():
    """Endpoint for submitting text correction
    ---
    post:
      description: Submit text correction for given id
      responses:
        202:
          description: Text correction is successfully submitted
          content:
            application/json:
              schema:
                type: TODO
                example: TODO
        400:
          description: Text correction request does not contain needed information
    """
    text_correction = request.json
    if 'id' not in text_correction or 'text' not in text_correction:
        return '', 400
    queue_service.send_text_correction(text_correction['id'], text_correction['text'])
    return '', 202
