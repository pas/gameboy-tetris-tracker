import unittest

import numpy as np
from PIL import Image

from tetristracker.tile.tiler import Tiler


class TestTiler(unittest.TestCase):
  def test_tiler(self):
    image = np.array(Image.open("test/scenario-2-high-res.png").convert('RGB'))
    tiler = Tiler(18, 10, image)
    assert(tiler.adapted_image.shape[0] == 18)
    assert(tiler.adapted_image.shape[1] == 10)
    self.assertEqual(tiler.tile_height, 53)
    self.assertEqual(tiler.tile_width, 53)