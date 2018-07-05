import os
import unittest
from io import BytesIO

class TestFloorPlanClassifierService(unittest.TestCase):
    def setUp(self):
        self.img_path = os.path.join(os.path.dirname(__file__), "test_image.jpeg")
        self.img_bytes = BytesIO(open(self.img_path, 'rb'))

    def test_classify(self):
        pass
