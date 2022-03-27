from flask import Blueprint

service_endpoint = Blueprint('service_endpoint', __name__, static_folder='../static')


@service_endpoint.route('/health', methods=['GET'])
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


@service_endpoint.route('/doc', methods=['GET'])
def doc():
    return service_endpoint.send_static_file('index.html')
