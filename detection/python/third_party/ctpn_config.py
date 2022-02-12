import os

# bgr can find from  here: https://github.com/fchollet/deep-learning-models/blob/master/imagenet_utils.py
IMAGE_MEAN = [123.68, 116.779, 103.939]

WEIGHTS_FILE = os.path.join(os.path.dirname(__file__), 'weights', 'CTPN.pth')
