import logging

from flask_app import app, register_blueprints, generate_doc
from endpoints.doc_endpoint import doc_endpoint
from endpoints.health_endpoint import health_endpoint, check_health
from endpoints.ocr_endpoint import ocr_endpoint, read_image, correct_text

logging.basicConfig(level=logging.INFO)

log = logging.getLogger(__name__)

register_blueprints(app, blueprints=[ocr_endpoint, health_endpoint, doc_endpoint])
generate_doc(app, doc_endpoints=[read_image, correct_text, check_health])

if __name__ == '__main__':
    app.run(debug=True)
