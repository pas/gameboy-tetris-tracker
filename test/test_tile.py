import unittest

import numpy as np
from PIL import Image

from tetristracker.tile.tile import Tile


class TestTile(unittest.TestCase):
  def test_tile_creation(self):
    tile_image = np.array(Image.open("test/tiles/T-mino-1.png").convert('L'))
    Tile(tile_image);

  def test_tile_center_grey(self):
    tile_image = np.array(Image.open("test/tiles/i-mino.png").convert('L'))
    tile = Tile(tile_image)
    self.assertTrue(tile.center_contains_grey())

  def test_tile_center_black(self):
    tile_image = np.array(Image.open("test/tiles/o-mino.png").convert('L'))
    tile = Tile(tile_image)
    self.assertFalse(tile.center_contains_grey())

  def test_tile_min_value_black(self):
    tile_image = np.array(Image.open("test/tiles/i-mino.png").convert('L'))
    tile = Tile(tile_image)
    self.assertEqual(tile.get_min(), 0)

  def test_tile_min_value_grey(self):
    tile_image = np.array(Image.open("test/tiles/i-mino-transition.png").convert('L'))
    tile = Tile(tile_image)
    self.assertGreater(tile.get_min(), 100)

  def test_tile_max_value_grey(self):
    tile_image = np.array(Image.open("test/tiles/i-mino.png").convert('L'))
    tile = Tile(tile_image)
    self.assertEqual(tile.get_max(), 183)

  def test_tile_max_value_white(self):
    tile_image = np.array(Image.open("test/tiles/T-mino-1.png").convert('L'))
    tile = Tile(tile_image)
    self.assertEqual(tile.get_max(), 255)

  def test_tile_grey_is_not_white(self):
    tile_image = np.array(Image.open("test/tiles/i-mino-transition.png").convert('L'))
    tile = Tile(tile_image)
    self.assertFalse(tile.is_white())

  def test_tile_dark_grey_is_not_black(self):
    tile_image = np.array(Image.open("test/tiles/l-mino.png").convert('L'))
    tile = Tile(tile_image)
    self.assertFalse(tile.is_black())

  def test_tile_not_one_color(self):
    tile_image = np.array(Image.open("test/tiles/T-mino-1.png").convert('L'))
    tile = Tile(tile_image);
    self.assertFalse(tile.is_one_color())

  def test_tile_one_color(self):
    tile_image = np.array(Image.open("test/tiles/tetris-tile-1.png").convert('L'))
    tile = Tile(tile_image);
    self.assertTrue(tile.is_one_color())

  def test_tile_one_color_2(self):
    tile_image = np.array(Image.open("test/tiles/tetris-tile-2.png").convert('L'))
    tile = Tile(tile_image);
    self.assertTrue(tile.is_one_color())

  def test_tile_dull(self):
    tile_image = np.array(Image.open("test/tiles/s-mino-line-clear.png").convert('L'))
    tile = Tile(tile_image);
    self.assertTrue(tile.is_dull())

  def test_tile_non_dull_t_mino(self):
    tile_image = np.array(Image.open("test/tiles/T-mino-1.png").convert('L'))
    tile = Tile(tile_image);
    self.assertFalse(tile.is_dull())

  def test_tile_non_dull_l_mino(self):
    tile_image = np.array(Image.open("test/tiles/L-mino-1.png").convert('L'))
    tile = Tile(tile_image);
    self.assertFalse(tile.is_dull())

  def test_tile_non_dull_l_mino(self):
    tile_image = np.array(Image.open("test/tiles/l-mino-2.png").convert('L'))
    tile = Tile(tile_image);
    self.assertFalse(tile.is_dull())

  def test_tile_dull_l_mino(self):
    tile_image = np.array(Image.open("test/tiles/L-mino-bright-transition.png").convert('L'))
    tile = Tile(tile_image);
    self.assertTrue(tile.is_dull())

  def test_tile_non_dull_i_mino(self):
    tile_image = np.array(Image.open("test/tiles/i-mino.png").convert('L'))
    tile = Tile(tile_image);
    self.assertFalse(tile.is_dull())

  def test_tile_non_dull_i_mino_2(self):
    tile_image = np.array(Image.open("test/tiles/i-mino-center.png").convert('L'))
    tile = Tile(tile_image);
    self.assertFalse(tile.is_dull())

  def test_tile_dull_i_mino(self):
    tile_image = np.array(Image.open("test/tiles/I-mino-line-clear.png").convert('L'))
    tile = Tile(tile_image);
    self.assertTrue(tile.is_dull())

  def test_tile_dull_o_mino(self):
    tile_image = np.array(Image.open("test/tiles/o-mino-line-clear.png").convert('L'))
    tile = Tile(tile_image);
    self.assertTrue(tile.is_dull())

  def test_tile_non_dull_o_mino(self):
    tile_image = np.array(Image.open("test/tiles/o-mino.png").convert('L'))
    tile = Tile(tile_image);
    self.assertFalse(tile.is_dull())