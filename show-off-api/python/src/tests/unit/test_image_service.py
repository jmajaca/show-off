import unittest

import numpy as np
from werkzeug.datastructures import FileStorage

from exceptions.exceptions import ImageDimensionsTooLargeError
from models.detection_api import MinimalTextBox
from services.image_service import ImageService


class TestImageService(unittest.TestCase):

    def setUp(self) -> None:
        self.image_service = ImageService()
        self.resource_path = '../resources'

    def test_cv2_convert(self):
        with open(f'{self.resource_path}/image_ok_dim.jpg', 'rb') as image:
            cv2_image = self.image_service.cv2_convert(FileStorage(stream=image))
            self.assertEqual(100, cv2_image.shape[0])
            self.assertEqual(100, cv2_image.shape[1])

    def test_check_dimensions_with_invalid_dimensions(self):
        image_array = np.empty((1001, 1001, 3))
        with self.assertRaises(ImageDimensionsTooLargeError) as context:
            self.image_service.check_dimensions(image_array)

    def test_check_dimensions_with_valid_dimensions(self):
        image_array = np.empty((100, 100, 3))
        self.image_service.check_dimensions(image_array)

    def test_cut_min_box_dimensions(self):
        og_height, og_width = 100, 100
        height, width = 25, 50
        image = np.empty((og_height, og_width, 1))
        box = MinimalTextBox(start_x=10, start_y=10, height=height, width=width)
        cut_image = self.image_service.cut_min_box(image, box)
        self.assertEqual(height, cut_image.shape[0])
        self.assertEqual(width, cut_image.shape[1])
        self.assertEqual(og_height, image.shape[0])
        self.assertEqual(og_width, image.shape[1])

    def test_cut_min_box_too_large_dimensions(self):
        og_height, og_width = 100, 100
        height, width = 200, 500
        image = np.empty((og_height, og_width, 1))
        box = MinimalTextBox(start_x=0, start_y=0, height=height, width=width)
        cut_image = self.image_service.cut_min_box(image, box)
        self.assertEqual(og_height, cut_image.shape[0])
        self.assertEqual(og_width, cut_image.shape[1])


if __name__ == '__main__':
    unittest.main()
