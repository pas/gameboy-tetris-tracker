import unittest

import numpy as np
from PIL import Image

from tetristracker.tile.tile import Tile


class TestTile(unittest.TestCase):
  def test_tile(self):
    tile_image = np.array(Image.open("test/tiles/T-mino-1.png").convert('L'))
    Tile(tile_image);

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