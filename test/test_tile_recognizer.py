import unittest

import numpy as np
from PIL import Image

from tetristracker.tile.tile_recognizer import TileRecognizer


class TestTileRecognizer(unittest.TestCase):
  def test_l_mino(self):
    recognizer = TileRecognizer()
    tile = np.array(Image.open("test/tiles/L-mino-1.png").convert('RGB'))
    result = recognizer.recognize(tile)

    self.assertEqual(result, 3)


  def test_t_mino(self):
    recognizer = TileRecognizer()
    tile = np.array(Image.open("test/tiles/T-mino-1.png").convert('RGB'))

    result = recognizer.recognize(tile)

    self.assertEqual(result, 4)
