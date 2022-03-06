import os

DETECTION_API_URL = os.environ['DETECTION_API_URL']
RECOGNITION_API_URL = os.environ['RECOGNITION_API_URL']

QUEUE_HOST = os.getenv('QUEUE_HOST', 'localhost')
QUEUE_PORT = os.getenv('QUEUE_PORT', '5672')
QUEUE_VIRTUAL_HOST = os.getenv('QUEUE_VIRTUAL_HOST', '/')
QUEUE_USERNAME = os.getenv('QUEUE_USERNAME', 'guest')
QUEUE_PASSWORD = os.getenv('QUEUE_PASSWORD', 'guest')

IMAGE_QUEUE_NAME = os.environ['IMAGE_QUEUE_NAME']
