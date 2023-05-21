import unittest

import cv2
import numpy as np
import yaml
from PIL import Image

from tetristracker.capturer.capturer import Capturer
from tetristracker.capturer.mss_capturer import MSSCapturer
from tetristracker.capturer.ocv_capturer import OCVCapturer


class StaticCapturer(Capturer):
  def __init__(self, image_path):
    self.static_image = np.array(Image.open(image_path).convert('RGB'))

  def grab_image(self):
    return self.static_image


class TestCapturer(unittest.TestCase):
  def test_cv_capturer(self):
    capturer = OCVCapturer()

  def test_mss_capturer(self):
    with open('config.yml', 'r') as config_file:
      configs = yaml.safe_load(config_file)
      bounding_box = configs["bounding_box"]

    capturer = MSSCapturer(bounding_box)
    image = capturer.grab_image()
    cv2.imwrite("screenshots/non-trimmed.png", image)
    image = capturer.trim(image)
    cv2.imwrite("screenshots/trimmed.png", image)