import unittest

from tetristracker.image.gameboy_image import GameboyImage


class TestGameboyImage(unittest.TestCase):
  def test_gameboy_image(self):
    processor = self.create_gameboy_view_processor()

    #get a tiled 4x4 image
    preview_image = processor.get_preview()

    gameboy_image = GameboyImage(preview_image, 4, 4, 53, 53, is_tiled=True)
    image = gameboy_image.untile()
    self.assertEqual(4*53, image.shape[0])
    self.assertEqual(4*53, image.shape[1])
    self.assertEqual(3, image.shape[2])

    image = gameboy_image.tile()
    self.assertEqual(4, image.shape[0])
    self.assertEqual(4, image.shape[1])
    self.assertEqual(53, image.shape[2])
    self.assertEqual(53, image.shape[3])
    self.assertEqual(3, image.shape[4])