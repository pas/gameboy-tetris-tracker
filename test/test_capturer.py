import unittest

import cv2
import numpy as np
import yaml
from PIL import Image

from tetristracker.capturer.capturer import Capturer
from tetristracker.capturer.mss_capturer import MSSCapturer
from tetristracker.capturer.interceptor_capturer import InterceptorCapturer
from tetristracker.capturer.video_file_capturer import VideoFileCapturer

from tetristracker.gui.stoppable_thread import StoppableThread
import time

from tetristracker.helpers.config import Config


class StaticCapturer(Capturer):
  def __init__(self, image_path):
    self.static_image = np.array(Image.open(image_path).convert('RGB'))

  def grab_image(self):
    return self.static_image


class TestCapturer(unittest.TestCase):
  def test_interceptor_capturer(self):
    config = Config(path="test/test-config.yml")
    capturer = InterceptorCapturer(config, create_temp_dir=False)
    image = capturer.grab_image()
    cv2.imwrite("screenshots/test-direct-capture.png", image)
    capturer.release()

  def test_video_file_capturer(self):
    file_name = "test/video/video-test-full-400k.mkv"
    bounding_box =  { "height": 467, "left": 73, "top": 127, "width": 518}
    capturer = VideoFileCapturer(file_name, bounding_box)
    frame = capturer.grab_image()
    print(len(frame), len(frame[0]))
    cv2.imwrite("screenshots/test-output-video.png", frame)

  def test_mss_capturer(self):
    with open('config.yml', 'r') as config_file:
      configs = yaml.safe_load(config_file)
      bounding_box = configs["screen"]["bounding_box"]

    capturer = MSSCapturer(bounding_box)
    image = capturer.grab_image()
    cv2.imwrite("screenshots/non-trimmed.png", image)
    image = capturer.trim(image)
    cv2.imwrite("screenshots/trimmed.png", image)

