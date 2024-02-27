import unittest

from test.helpers import get_image, create_gameboy_view_processor_with
from tetristracker.image.gameboy_image import GameboyImage
from tetristracker.processor.number_processor import SequentialNumberProcessor, NumberProcessor, \
  SimplisticSequentialNumberProcessor


class TestGameboyViewProcessor(unittest.TestCase):
  def get_tiled_image(self, path, number_of_tiles_height, number_of_tiles_width, tile_height, tile_width):
    image = get_image(path)
    gb_image = GameboyImage(image, number_of_tiles_height, number_of_tiles_width, tile_height, tile_width, is_tiled=False)
    return gb_image.tile()

  def get_tiled_image_from_full_view(self, path):
    gb_view = create_gameboy_view_processor_with(path)
    return gb_view.get_score()

  def test_number_processor_score_98(self):
    # Currently not fixable but not used anymore
    # I'll leave it in to showcase the problem
    # of the non-sequential ocr version.
    image = get_image("test/numbers/98.png")
    processor = NumberProcessor(image)
    result = processor.get_number()
    self.assertEqual(98, result, "This test is currently not fixable and the reason why I changed from full OCR to sequential OCR.")

  def test_sequential_number_processor_score_17_ocr_capturer(self):
    image = self.get_tiled_image("test/numbers/17-ocr-capturer.png", 1, 6, 64, 64)
    processor = SequentialNumberProcessor(image)
    result = processor.get_number()
    self.assertEqual(17, result)

  def test_simplistic_sequential_number_processor_unknown_score(self):
    score = self.get_tiled_image_from_full_view("test/full-view/gameboy-full-view-problematic-score-in-transition-ocv-capturer.png")
    processor = SimplisticSequentialNumberProcessor(score)
    result = processor.get_number()
    self.assertIsNone(result)

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

  def test_sequential_number_processor_scores(self):
    files = [
      ["98.png", 98],
      ["15600.png", 15600],
      ["19083.png", 19083],
      ["102839.png", 102839],
      ["12097.png", 12097],
    ]

    for i in range(0, len(files)):
      image = self.get_tiled_image("test/numbers/" + files[i][0], 1, 6, 48, 48)
      processor = SequentialNumberProcessor(image)
      result = processor.get_number()
      self.assertEqual(files[i][1], result)

  def test_simplistic_sequential_number_processor_unknown_scores(self):
    files = [
      "transition-third-number.png",
      "transition-multiple-numbers.png",
      "transition-faint.png",
      "transition-first-and-second-number.png",
      "transition-second-number.png",
      "transition-first-and-second-number-2.png",
      "transition-first-and-second-number-3.png",
      "transition-second-and-third-number.png"
    ]
    for i in range(0, len(files)):
      with self.subTest(i=i):
        image = self.get_tiled_image("test/numbers/" + files[i], 1, 6, 39, 39)
        processor = SimplisticSequentialNumberProcessor(image)
        result = processor.get_number()
        self.assertIsNone(result)


  def test_simplistic_sequential_number_processor_scores(self):
    files = [
      ["98.png", 98],
      ["15600.png", 15600],
      ["19083.png", 19083],
      ["102839.png", 102839],
      ["12097.png", 12097],
    ]

    for i in range(0, len(files)):
      image = self.get_tiled_image("test/numbers/" + files[i][0], 1, 6, 48, 48)
      processor = SimplisticSequentialNumberProcessor(image)
      result = processor.get_number()
      self.assertEqual(files[i][1], result)

  def test_number_processor_scores(self):
    files = [
      ["15600.png", 15600],
      ["19083.png", 19083],
      ["102839.png", 102839]
    ]

    for i in range(0, len(files)):
      image = get_image("test/numbers/" + files[i][0])
      processor = NumberProcessor(image)
      result = processor.get_number()
      self.assertEqual(files[i][1], result)