import unittest
import shutil
import os

from tetristracker.helpers.config import Config

class TestConfig(unittest.TestCase):
  def setUp(self):
    # copy test yaml file
    shutil.copyfile("test/test-config.yml", "test/temp-test-config.yml")

  def tearDown(self):
    # delete test yaml file
    os.remove("test/temp-test-config.yml")

  def _init_config(self):
    return Config("test/temp-test-config.yml")

  def test_get_screen__bounding_box(self):
      config = self._init_config()
      bounding_box = config.get_screen_bounding_box()

      self.assertEqual(1000, bounding_box["height"])
      self.assertEqual(2000, bounding_box["left"])
      self.assertEqual(3000, bounding_box["top"])
      self.assertEqual(4000, bounding_box["width"])

  def test_set_screen_bounding_box(self):
    bounding_box = { 'top' : 100, 'left' : 200, 'width': 300, 'height': 400 }
    config = self._init_config()
    config.set_screen_bounding_box(bounding_box)

  def test_get_capturer(self):
      config = self._init_config()
      capturer = config.get_capturer()

      self.assertEqual("screen", capturer)

  def test_set_capturer(self):
      config = self._init_config()
      config.set_capturer("interceptor")

      capturer = config.get_capturer()
      self.assertEqual("interceptor", capturer)