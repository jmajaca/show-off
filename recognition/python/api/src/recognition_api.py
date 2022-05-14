import json
import logging
import os

import opentracing as opentracing
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
from flask import Flask
from flask_opentracing import FlaskTracer

from jaeger_client import Config

import env_api
from endpoints.recognition_endpoint import recognition_endpoint, extract
from endpoints.service_endpoint import service_endpoint, check_health

app = Flask(__name__)
app.register_blueprint(service_endpoint)
app.register_blueprint(recognition_endpoint)

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


def initialize_tracer() -> opentracing.Tracer:
    config = Config(config={
            'sampler': {
                'type': 'const',
                'param': 1
            },
            'reporter_batch_size': 1,
        }, service_name=env_api.JAEGER_SERVICE_NAME)
    return config.initialize_tracer()


tracing = FlaskTracer(tracer=lambda: initialize_tracer(), trace_all_requests=True, app=app)


if __name__ == '__main__':
    app.run(debug=True)
