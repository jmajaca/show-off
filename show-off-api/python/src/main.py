import json
import logging
import os

import opentracing
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
from flask import Flask
from flask_cors import CORS
from flask_opentracing import FlaskTracer
from jaeger_client import Config

from endpoints.doc_endpoint import doc_endpoint
from endpoints.health_endpoint import health_endpoint, check_health
from endpoints.ocr_endpoint import ocr_endpoint, read_image, correct_text

logging.basicConfig(level=logging.INFO)

log = logging.getLogger(__name__)

spec = APISpec(
    title='Show Off API',
    version='v1',
    plugins=[FlaskPlugin(), MarshmallowPlugin()],
    openapi_version='3.0.3'
)


def create_app():
    app = Flask(__name__)
    app.register_blueprint(ocr_endpoint)
    app.register_blueprint(health_endpoint)
    app.register_blueprint(doc_endpoint)

    with app.test_request_context():
        spec.path(view=read_image)
        spec.path(view=correct_text)
        spec.path(view=check_health)

    dir_path = os.path.dirname(os.path.realpath(__file__))
    with open(dir_path + '/doc/swagger.json', 'w') as f:
        json.dump(spec.to_dict(), f)

    return app


def initialize_tracer() -> opentracing.Tracer:
    config = Config(config={
            'sampler': {
                'type': 'const',
                'param': 1
            },
            'logging': True,
            'reporter_batch_size': 1,
        }, service_name='show-off-api')
    return config.initialize_tracer()


app = create_app()
CORS(app)
flask_tracer = FlaskTracer(tracer=initialize_tracer(), trace_all_requests=True, app=app)


if __name__ == '__main__':
    app.run(debug=True)
