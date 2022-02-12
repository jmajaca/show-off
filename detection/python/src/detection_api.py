import json
import os
import logging

from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
from flask import Flask, request, jsonify
from flask_cors import CORS

from python.src.detection import Detection

app = Flask(__name__, static_folder='static')
CORS(app)

spec = APISpec(
    title='Show Off API',
    version='v1',
    plugins=[FlaskPlugin(), MarshmallowPlugin()],
    openapi_version='3.0.3'
)


@app.route('/boxes', methods=['POST'])
def determine_boxes():
    """Endpoint for determining text boxes on image
    ---
    post:
      description: For given image return text boxes
      responses:
        200:
          description: Process of determining text boxes completed successfully
        404:
          description: Invalid image has been sent
        500:
          description: Error occurred while in process of determining text boxes
    """
    try:
        files = request.files.to_dict()
        image = files['image']
        image_string = image.read()
    except Exception as e:
        logging.warning('Invalid image file sent', e)
        return '', 404
    boxes = Detection.get_text_boxes(image_string)
    result = []
    for index, box in enumerate(boxes):
        points = list(map(int, box[:-1]))
        points = [{'axis_x': points[i], 'axis_y': points[i+1]} for i in range(0, len(points), 2)]
        element = {'ord_num': index, 'points': points, 'probability': round(box[-1], 4)}
        result.append(element)
    return jsonify(result), 200


@app.route('/health', methods=['GET'])
def check_health():
    """Endpoint for checking if application is up and running
    ---
    get:
      description: Check if app is running
      responses:
        200:
          description: App is running
    """
    return '', 200


@app.route('/doc')
def doc():
    return app.send_static_file('index.html')


with app.test_request_context():
    spec.path(view=determine_boxes)
    spec.path(view=check_health)

dir_path = os.path.dirname(os.path.realpath(__file__))
with open(dir_path + '/static/swagger.json', 'w') as f:
    json.dump(spec.to_dict(), f)

if __name__ == '__main__':
    app.run(debug=True)
