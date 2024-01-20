import unittest

import cv2
import numpy as np
import yaml
from PIL import Image

from tetristracker.capturer.capturer import Capturer
from tetristracker.capturer.mss_capturer import MSSCapturer
from tetristracker.capturer.interceptor_capturer import InterceptorCapturer
from tetristracker.capturer.video_file_capturer import VideoFileCapturer
import threading

from tetristracker.gui.stoppable_thread import StoppableThread
import time


class StaticCapturer(Capturer):
  def __init__(self, image_path):
    self.static_image = np.array(Image.open(image_path).convert('RGB'))

  def grab_image(self):
    return self.static_image


class TestCapturer(unittest.TestCase):
  def test_cv_capturer(self):
    capturer = InterceptorCapturer()
    image = capturer.grab_image()
    cv2.imwrite("screenshots/test-direct-capture.png", image)

  def test_video_file_capturer(self):
    file_name = "video-capturer-example.mp4"
    capturer = VideoFileCapturer(file_name)
    frame = capturer.grab_image()
    print(frame)

  def test_mss_capturer(self):
    with open('config.yml', 'r') as config_file:
      configs = yaml.safe_load(config_file)
      bounding_box = configs["bounding_box"]

    capturer = MSSCapturer(bounding_box)
    image = capturer.grab_image()
    cv2.imwrite("screenshots/non-trimmed.png", image)
    image = capturer.trim(image)
    cv2.imwrite("screenshots/trimmed.png", image)

  def test_mss_capturer_in_thread(self):
    with open('config.yml', 'r') as config_file:
      configs = yaml.safe_load(config_file)
      bounding_box = configs["bounding_box"]

    capturer = MSSCapturer(bounding_box)
    thread = StoppableThread(target=threaded_capturing_function, args=(capturer,), daemon=True)
    thread.start()
    time.sleep(10)
    thread.join()

def threaded_capturing_function(capturer):
  image = capturer.grab_image()
  cv2.imwrite("screenshots/non-trimmed-threaded.png", image)

