from flask import Blueprint

ocr_endpoint = Blueprint('ocr_endpoint', __name__)


@ocr_endpoint.route('/read', methods=['POST'])
def read():
    pass


@ocr_endpoint.route('/correct-text', methods=['POST'])
def correct_text():
    pass
