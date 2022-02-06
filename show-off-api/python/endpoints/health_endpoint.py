from flask import Blueprint

health_endpoint = Blueprint('health_endpoint', __name__)


@health_endpoint.route('/health', methods=['GET'])
def check_health():
    """Endpoint for checking if application is up and running
    ---
    get:
      description: Check if app is running
      responses:
        200:
          description: App is running
    """
    return 200
