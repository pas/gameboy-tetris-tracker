import unittest

import numpy as np
from PIL import Image, ImageEnhance

from test.helpers import create_gameboy_view_processor_with, write_image
from tetristracker.image.gameboy_image import GameboyImage
from tetristracker.processor.gameboy_view_processor import GameboyViewProcessor
from tetristracker.processor.number_processor import SequentialNumberProcessor


class TestGameboyViewProcessor(unittest.TestCase):
  def test_gameboy_view_processor_on_pause(self):
      image = np.array(Image.open("test/full-view/gameboy-pause-full-view.png").convert('RGB'))
      processor = GameboyViewProcessor(image)
      continue_image = processor.get_continue()
      gameboy_image = GameboyImage(continue_image, 8, 4, 53, 53, is_tiled=True)
      number_process = SequentialNumberProcessor(gameboy_image.image)
      self.assertEqual(871406, number_process.get_number())