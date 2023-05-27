import unittest

import numpy as np
from PIL import Image

from test.helpers import create_gameboy_view_processor_with
from tetristracker.processor.preview_processor import PreviewProcessor
from tetristracker.tile.tile_recognizer import TileRecognizer


class TestPreviewProcessor(unittest.TestCase):
  def create_processor_with(self, path):
    image = np.array(Image.open(path).convert('RGB'))
    return PreviewProcessor(image)

  def run_preview_processor_with(self, path):
    processor = self.create_processor_with(path)
    return processor.run(), processor

  def test_preview_processor_from_gameboy_view_processor (self):
    processor = create_gameboy_view_processor_with("test/full-view/gameboy-full-view.png")

    preview_image = processor.get_preview()
    preview_processor = PreviewProcessor(preview_image, image_is_tiled=True)
    preview = preview_processor.run()
    self.assertEqual(preview, TileRecognizer.T_MINO)

  def test_preview_processor_4x4tiles(self):
    preview_processor = self.create_processor_with("test/preview/t-to-l-tetromino-transition-preview.png")
    self.assertEqual(4, preview_processor.nr_of_tiles_height)
    self.assertEqual(4, preview_processor.nr_of_tiles_width)

  def test_preview_processor_ambigous(self):
    _, preview_processor = self.run_preview_processor_with("test/preview/t-to-l-tetromino-transition-preview.png")
    self.assertTrue(preview_processor.ambiguous)

  def test_preview_processor_z(self):
    result, preview_processor = self.run_preview_processor_with("test/preview/z-tetromino-preview.png")
    self.assertEqual(result, TileRecognizer.Z_MINO)
    self.assertFalse(preview_processor.ambiguous)

  def test_preview_processor_l(self):
    result, preview_processor = self.run_preview_processor_with("test/preview/l-tetromino-preview.png")
    self.assertEqual(result, TileRecognizer.L_MINO)
    self.assertFalse(preview_processor.ambiguous)

  def test_preview_processor_j(self):
    result, preview_processor = self.run_preview_processor_with("test/preview/j-tetromino-preview.png")
    self.assertEqual(result, TileRecognizer.J_MINO)
    self.assertFalse(preview_processor.ambiguous)

  def test_preview_processor_s(self):
    result, preview_processor = self.run_preview_processor_with("test/preview/s-tetromino-preview.png")
    self.assertEqual(result, TileRecognizer.S_MINO)
    self.assertFalse(preview_processor.ambiguous)

  def test_preview_processor_o(self):
    result, preview_processor = self.run_preview_processor_with("test/preview/o-tetromino-preview.png")
    self.assertEqual(result, TileRecognizer.O_MINO)
    self.assertFalse(preview_processor.ambiguous)

  def test_preview_processor_i(self):
    result, preview_processor = self.run_preview_processor_with("test/preview/i-tetromino-preview.png")
    self.assertEqual(result, TileRecognizer.I_MINO_SIMPLE)
    self.assertFalse(preview_processor.ambiguous)

  def test_preview_processor_t(self):
    result, preview_processor = self.run_preview_processor_with("test/preview/t-tetromino-preview.png")
    self.assertEqual(result, TileRecognizer.T_MINO)
    self.assertFalse(preview_processor.ambiguous)
