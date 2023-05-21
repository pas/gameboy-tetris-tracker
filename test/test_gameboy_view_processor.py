import unittest

import numpy as np
from PIL import Image

from tetristracker.image.gameboy_image import GameboyImage
from tetristracker.processor.gameboy_view_processor import GameboyViewProcessor
from tetristracker.processor.number_processor import NumberProcessor


class TestGameboyViewProcessor(unittest.TestCase):
  def test_gameboy_view_processor_on_pause(self):
      image = np.array(Image.open("test/full-view/gameboy-pause-full-view.png").convert('RGB'))
      processor = GameboyViewProcessor(image)
      continue_image = processor.get_continue()
      gameboy_image = GameboyImage(continue_image, 8, 4, 53, 53, is_tiled=True)
      gameboy_image.untile()
      number_process = NumberProcessor(gameboy_image.image)
      self.assertEqual(71006 ,number_process.get_number())