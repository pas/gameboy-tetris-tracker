import unittest

import numpy as np
from PIL import Image

from tetristracker.game import Round
from tetristracker.processor.gameboy_view_processor import GameboyViewProcessor

class MockWriter():
  def restart(self):
    pass

class TestGame(unittest.TestCase):
  def test_get_level_9_heart(self):
      image = np.array(Image.open("test/full-view/gameboy-full-view-level-9-heart.png").convert('RGB'))
      processor = GameboyViewProcessor(image)
      level, is_heart = Round(None, None, None, MockWriter()).level(processor)
      self.assertEqual(9, level)
      self.assertTrue(is_heart)

  def test_get_level_10(self):
    image = np.array(Image.open("test/full-view/gameboy-full-view-in-transition-problematic.png").convert('RGB'))
    processor = GameboyViewProcessor(image)
    level, is_heart = Round(None, None, None, MockWriter()).level(processor)
    self.assertEqual(10, level)
    self.assertFalse(is_heart)