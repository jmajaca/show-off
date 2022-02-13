import logging
from datetime import datetime

from flask import Blueprint, request
from flask_cors import cross_origin

from api.api import DetectionAPI
from exceptions.exceptions import ImageDimensionsTooLargeError
from utils.image_utils import ImageUtils

ocr_endpoint = Blueprint('ocr_endpoint', __name__)

detection_api = DetectionAPI()


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
    files = request.files.to_dict()
    image = files['image']
    cv2_image = ImageUtils.cv2_convert(image)
    try:
        ImageUtils.check_dimensions(cv2_image)
    except ImageDimensionsTooLargeError as e:
        logging.error('Invalid image', e)
        return {'timestamp': datetime.now(), 'error': str(e)}, 400
    text_boxes = detection_api.get_text_boxes(image)
    for i, box in enumerate(text_boxes):
        cut_image = ImageUtils.cut_box(cv2_image, box)
    return {}, 200


@ocr_endpoint.route('/correct-text', methods=['POST'])
@cross_origin()
def correct_text():
    return '', 404
