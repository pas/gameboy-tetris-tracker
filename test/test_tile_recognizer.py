import unittest

import numpy as np
from PIL import Image

from tetristracker.tile.tile import Tile
from tetristracker.tile.tile_recognizer import TileRecognizer


class TestTileRecognizer(unittest.TestCase):
  def test_l_mino(self):
    recognizer = TileRecognizer()
    tile = np.array(Image.open("test/tiles/L-mino-1.png").convert('L'))

    result = recognizer.recognize(tile)

    self.assertEqual(result, 3)


  def test_t_mino(self):
    recognizer = TileRecognizer()
    tile = np.array(Image.open("test/tiles/T-mino-1.png").convert('L'))

    result = recognizer.recognize(tile)

    self.assertEqual(result, 4)

  def test_finished_mino(self):
    recognizer = TileRecognizer()
    tile_image = np.array(Image.open("test/tiles/finished-tile.png").convert('L'))

    self.assertTrue(recognizer.is_finished_tile(tile_image))

  def test_non_finished_l_mino(self):
    recognizer = TileRecognizer()
    tile_image = np.array(Image.open("test/tiles/T-mino-1.png").convert('L'))

    self.assertFalse(recognizer.is_finished_tile(tile_image))

  def test_non_finished_t_mino(self):
    recognizer = TileRecognizer()
    tile_image = np.array(Image.open("test/tiles/T-mino-1.png").convert('L'))

    self.assertFalse(recognizer.is_finished_tile(tile_image))
