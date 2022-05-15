import json
import os
import logging
from datetime import datetime

import opentracing as opentracing
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_opentracing import FlaskTracer
from typing import Tuple

from jaeger_client import Config

import env
from api_schemas import *
from detection_service import DetectionService
from exceptions import InvalidImageError

app = Flask(__name__, static_folder='static')
CORS(app)

spec = APISpec(
    title='Detection API',
    version='v1',
    plugins=[FlaskPlugin(), MarshmallowPlugin()],
    openapi_version='3.0.3'
)


def initialize_tracer() -> opentracing.Tracer:
    config = Config(config={
            'sampler': {
                'type': 'const',
                'param': 1
            },
            'reporter_batch_size': 1,
        }, service_name=env.JAEGER_SERVICE_NAME)
    return config.initialize_tracer()


tracing = FlaskTracer(tracer=lambda: initialize_tracer(), trace_all_requests=True, app=app)


@app.route('/boxes', methods=['POST'])
def determine_boxes():
    """Endpoint for determining text boxes on image
    ---
    post:
      description: For given image return text boxes
      requestBody:
        content:
          multipart/form-data:
            schema: TextBoxRequestSchema
      responses:
        200:
          description: Process of determining text boxes completed successfully
          content:
            application/json:
              schema: TextBoxSchema
        400:
          description: Invalid image has been sent
          content:
            application/json:
              schema: ErrorSchema
        500:
          description: Error occurred while in process of determining text boxes
    """
    try:
        files = request.files.to_dict()
        image_string = DetectionService.read_image_as_string(files)
        result = DetectionService.configure_box_response(image_string)
        return jsonify(result), 200
    except InvalidImageError as e:
        logging.warning('Invalid image file sent', exc_info=True)
        return create_error_response(e, 400)
    except Exception as e:
        logging.error('Error occurred while determining text boxes', exc_info=True)
        return create_error_response(e, 500)


@app.route('/minimal-boxes', methods=['POST'])
def determine_minimal_boxes():
    """Endpoint for determining minimal text boxes on image
    ---
    post:
      description: For given image return minimal text boxes
      requestBody:
        content:
          multipart/form-data:
            schema: TextBoxRequestSchema
      responses:
        200:
          description: Process of determining minimal text boxes completed successfully
          content:
            application/json:
              schema: MinimalTextBoxSchema
        400:
          description: Invalid image has been sent
          content:
            application/json:
              schema: ErrorSchema
        500:
          description: Error occurred while in process of determining minimal text boxes
    """
    try:
        logging.info(request.headers)
        files = request.files.to_dict()
        image_string = DetectionService.read_image_as_string(files)
        result = DetectionService.configure_box_response(image_string, 'minimal')
        return jsonify(result), 200
    except InvalidImageError as e:
        logging.warning('Invalid image file sent', exc_info=True)
        return create_error_response(e, 400)
    except Exception as e:
        logging.error('Error occurred while determining minimal text boxes', exc_info=True)
        return create_error_response(e, 500)


@app.route('/health', methods=['GET'])
def check_health():
    """Endpoint for checking if application is up and running
    ---
    get:
      description: Check if app is running
      responses:
        200:
          description: App is running
        500:
          description: App is not running
    """
    return '', 200


@app.route('/doc')
def doc():
    return app.send_static_file('index.html')


def create_error_response(e: Exception, status: int) -> Tuple[dict, int]:
    return {'timestamp': datetime.now(), 'error': str(e)}, status


with app.test_request_context():
    spec.path(view=determine_boxes)
    spec.path(view=determine_minimal_boxes)
    spec.path(view=check_health)

dir_path = os.path.dirname(os.path.realpath(__file__))
with open(dir_path + '/static/swagger.json', 'w') as f:
    json.dump(spec.to_dict(), f)

if __name__ == '__main__':
    app.run(debug=True)
