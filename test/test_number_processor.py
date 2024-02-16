import unittest

from test.helpers import get_image
from tetristracker.image.gameboy_image import GameboyImage
from tetristracker.processor.number_processor import SequentialNumberProcessor, NumberProcessor, \
  SimplisticSequentialNumberProcessor


class TestGameboyViewProcessor(unittest.TestCase):
  def get_tiled_image(self, path, number_of_tiles_height, number_of_tiles_width, tile_height, tile_width):
    image = get_image(path)
    gb_image = GameboyImage(image, number_of_tiles_height, number_of_tiles_width, tile_height, tile_width, is_tiled=False)
    return gb_image.tile()

  def test_number_processor_score_98(self):
    # Currently not fixable but not used anymore
    # I'll leave it in to showcase the problem
    # of the non-sequential ocr version.
    image = get_image("test/numbers/98.png")
    processor = NumberProcessor(image)
    result = processor.get_number()
    self.assertEqual(98, result, "This test is currently not fixable and the reason why I changed from full OCR to sequential OCR.")

  def test_sequential_number_processor_score_98(self):
    image = self.get_tiled_image("test/numbers/98.png", 1, 6, 48, 48)
    processor = SequentialNumberProcessor(image)
    result = processor.get_number()
    self.assertEqual(98, result)

  def test_simplistic_sequential_number_processor_score_98(self):
    image = self.get_tiled_image("test/numbers/98.png", 1, 6, 48, 48)
    processor = SimplisticSequentialNumberProcessor(image)
    result = processor.get_number()
    self.assertEqual(98, result)

  def test_sequential_number_processor_score_17_ocr_capturer(self):
    image = self.get_tiled_image("test/numbers/17-ocr-capturer.png", 1, 6, 64, 64)
    processor = SequentialNumberProcessor(image)
    result = processor.get_number()
    self.assertEqual(17, result)

  def test_simplistic_sequential_number_processor_score_17_ocr_capturer(self):
    image = self.get_tiled_image("test/numbers/17-ocr-capturer.png", 1, 6, 64, 64)
    processor = SimplisticSequentialNumberProcessor(image)
    result = processor.get_number()
    self.assertEqual(17, result)

  def test_number_processor_score_9(self):
    image = get_image("test/numbers/9.png")
    processor = NumberProcessor(image)
    result = processor.get_number()
    self.assertEqual(9, result)

  def test_sequential_number_processor_score_9(self):
    image = self.get_tiled_image("test/numbers/9.png", 1, 3, 35, 35)
    processor = SequentialNumberProcessor(image)
    result = processor.get_number()
    self.assertEqual(9, result)

  def test_simplistic_sequential_number_processor_score_9(self):
    image = self.get_tiled_image("test/numbers/9.png", 1, 3, 35, 35)
    processor = SimplisticSequentialNumberProcessor(image)
    result = processor.get_number()
    self.assertEqual(9, result)

  def test_sequential_number_processor_score_10739(self):
    image = self.get_tiled_image("test/numbers/10739.png", 1, 6, 38, 38)
    processor = SequentialNumberProcessor(image)
    result = processor.get_number()
    self.assertEqual(10739, result)

  def test_simplistic_sequential_number_processor_score_10739(self):
    image = self.get_tiled_image("test/numbers/10739.png", 1, 6, 38, 38)
    processor = SimplisticSequentialNumberProcessor(image)
    result = processor.get_number()
    self.assertEqual(10739, result)

  def test_number_processor_score_15600(self):
    image = get_image("test/numbers/15600.png")
    processor = NumberProcessor(image)
    result = processor.get_number()
    self.assertEqual(15600, result)

  def test_sequential_number_processor_score_15600(self):
    image = self.get_tiled_image("test/numbers/15600.png", 1, 6, 48, 48)
    processor = SequentialNumberProcessor(image)
    result = processor.get_number()
    self.assertEqual(15600, result)

  def test_simplistic_sequential_number_processor_score_15600(self):
    image = self.get_tiled_image("test/numbers/15600.png", 1, 6, 48, 48)
    processor = SimplisticSequentialNumberProcessor(image)
    result = processor.get_number()
    self.assertEqual(15600, result)

  def test_number_processor_score_19083(self):
    image = get_image("test/numbers/19083.png")
    processor = NumberProcessor(image)
    result = processor.get_number()
    self.assertEqual(19083, result)

  def test_sequential_number_processor_score_19083(self):
    image = self.get_tiled_image("test/numbers/19083.png", 1, 6, 48, 48)
    processor = SequentialNumberProcessor(image)
    result = processor.get_number()
    self.assertEqual(19083, result)

  def test_simplistic_sequential_number_processor_score_19083(self):
    image = self.get_tiled_image("test/numbers/19083.png", 1, 6, 48, 48)
    processor = SimplisticSequentialNumberProcessor(image)
    result = processor.get_number()
    self.assertEqual(19083, result)

  def test_number_processor_score_102839(self):
    image = get_image("test/numbers/102839.png")
    processor = NumberProcessor(image)
    result = processor.get_number()
    self.assertEqual(102839, result)

  def test_sequential_number_processor_score_102839(self):
    image = self.get_tiled_image("test/numbers/102839.png", 1, 6, 48, 48)
    processor = SequentialNumberProcessor(image)
    result = processor.get_number()
    self.assertEqual(102839, result)

  def test_simplistic_sequential_number_processor_score_102839(self):
    image = self.get_tiled_image("test/numbers/102839.png", 1, 6, 48, 48)
    processor = SimplisticSequentialNumberProcessor(image)
    result = processor.get_number()
    self.assertEqual(102839, result)

  def test_number_processor_score_12097(self):
    image = get_image("test/numbers/12097.png")
    processor = NumberProcessor(image)
    result = processor.get_number()
    self.assertEqual(12097, result)

  def test_sequential_number_processor_score_12097(self):
    image = self.get_tiled_image("test/numbers/12097.png", 1, 6, 48, 48)
    processor = SequentialNumberProcessor(image)
    result = processor.get_number()
    self.assertEqual(12097, result)

  def test_simplistic_sequential_number_processor_score_12097(self):
    image = self.get_tiled_image("test/numbers/12097.png", 1, 6, 48, 48)
    processor = SimplisticSequentialNumberProcessor(image)
    result = processor.get_number()
    self.assertEqual(12097, result)