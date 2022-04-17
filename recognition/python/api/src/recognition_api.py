import json
import logging
import os

from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
from flask import Flask
from flask_cors import CORS

from endpoints.recognition_endpoint import recognition_endpoint, extract
from endpoints.service_endpoint import service_endpoint, check_health

app = Flask(__name__)
app.register_blueprint(service_endpoint)
app.register_blueprint(recognition_endpoint)

CORS(app)

logging.basicConfig(level=logging.INFO)

spec = APISpec(
    title='Recognition API',
    version='v1',
    plugins=[FlaskPlugin(), MarshmallowPlugin()],
    openapi_version='3.0.3'
)


with app.test_request_context():
    spec.path(view=extract)
    spec.path(view=check_health)

dir_path = os.path.dirname(os.path.realpath(__file__))
with open(dir_path + '/static/swagger.json', 'w') as f:
    json.dump(spec.to_dict(), f)


if __name__ == '__main__':
    app.run(debug=True)
