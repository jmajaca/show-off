import json
import os

import opentracing
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
from flask import Flask
from flask_cors import CORS
from flask_opentracing import FlaskTracer
from jaeger_client import Config

from schema.schemas import *

import env

spec = APISpec(
    title='Show Off API',
    version='v1',
    plugins=[FlaskPlugin(), MarshmallowPlugin()],
    openapi_version='3.0.3'
)


def register_blueprints(flask_app: Flask, blueprints: list) -> None:
    for blueprint in blueprints:
        flask_app.register_blueprint(blueprint)


def generate_doc(flask_app: Flask, doc_endpoints: list) -> None:
    with flask_app.test_request_context():
        for doc_endpoint in doc_endpoints:
            spec.path(view=doc_endpoint)

    dir_path = os.path.dirname(os.path.realpath(__file__))
    with open(dir_path + '/doc/swagger.json', 'w') as f:
        json.dump(spec.to_dict(), f)


app = Flask(__name__)
CORS(app)


def initialize_tracer() -> opentracing.Tracer:
    config = Config(config={
        'sampler': {
            'type': 'const',
            'param': 1
        },
        'logging': True,
        'reporter_batch_size': 1,
    }, service_name=env.JAEGER_SERVICE_NAME)
    return config.initialize_tracer()


tracing = FlaskTracer(tracer=lambda: initialize_tracer(), trace_all_requests=True, app=app)


def set_tracing_endpoints(endpoints: list) -> None:
    for endpoint in endpoints:
        tracing.trace(endpoint)
