import json

from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
from flask import Flask

from endpoints.doc_endpoint import doc_endpoint
from endpoints.health_endpoint import health_endpoint, check_health
from endpoints.ocr_endpoint import ocr_endpoint

spec = APISpec(
    title='Show Off API',
    version='v1',
    plugins=[FlaskPlugin(), MarshmallowPlugin()],
    openapi_version='3.0.3'
)

app = Flask(__name__)
app.register_blueprint(ocr_endpoint)
app.register_blueprint(health_endpoint)
app.register_blueprint(doc_endpoint)

with app.test_request_context():
    spec.path(view=check_health)

with open('doc/swagger.json', 'w') as f:
    json.dump(spec.to_dict(), f)

if __name__ == '__main__':
    app.run(debug=True)
