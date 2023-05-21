import unittest

import cv2
import numpy as np
from PIL import Image

from tetristracker.image.image_manipulator import convert_to_4bitgrey


class TestImageManipulator(unittest.TestCase):
  def test_image_manipulator(self):
    image = np.array(Image.open("test/full-view/gameboy-full-view.png").convert('RGB'))
    image = convert_to_4bitgrey(image)
    print(image)
    cv2.imwrite("screenshots/reduced_grey_scale.png", image)