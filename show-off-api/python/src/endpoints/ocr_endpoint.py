from flask import Blueprint, request
from flask_cors import cross_origin

ocr_endpoint = Blueprint('ocr_endpoint', __name__)


@ocr_endpoint.route('/read', methods=['POST'])
@cross_origin()
def read():
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
    """
    files = request.files.to_dict()
    image = files['image']
    return {}, 200


@ocr_endpoint.route('/correct-text', methods=['POST'])
@cross_origin()
def correct_text():
    pass
