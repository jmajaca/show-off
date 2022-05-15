import os

model_weights_path = os.environ['MODEL_WEIGHTS_PATH']

JAEGER_SERVICE_NAME = os.getenv('JAEGER_SERVICE_NAME', 'recognition-api')
