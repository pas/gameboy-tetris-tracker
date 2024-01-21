import unittest

from test.helpers import create_gameboy_view_processor_with
from tetristracker.processor.preview_processor import PreviewProcessor
from tetristracker.tile.tile_recognizer import TileRecognizer


class TestPreviewTracker(unittest.TestCase):
  def test_preview_tracker_full_game(self):
    processor = create_gameboy_view_processor_with("test/full-view/gameboy-full-view.png")

    preview_image = processor.get_preview()
    preview_processor = PreviewProcessor(preview_image, image_is_tiled=True)
    preview = preview_processor.run()
    self.assertEqual(preview, TileRecognizer.T_MINO)
