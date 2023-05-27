import unittest

from test.helpers import create_testing_array_s2, create_testing_array_s1, create_testing_array_full_view_2, \
  create_testing_array_full_view, get_image, create_gameboy_view_processor_with, get_number
from tetristracker.processor.playfield_processor import PlayfieldProcessor
from tetristracker.processor.gameboy_view_processor import GameboyViewProcessor
from PIL import Image
import numpy as np


class TestPlayfieldProcessor(unittest.TestCase):
  def test_playfield_line_clear_detection(self):
    processor = create_gameboy_view_processor_with("test/full-view/gameboy-full-view-tetris.png")
    playfield_processor = PlayfieldProcessor(processor.get_playfield(), image_is_tiled=True)
    playfield = playfield_processor.run()
    self.assertEqual(1, playfield.line_clear_count)
    self.assertTrue(playfield.is_line_clear())

  def test_playfield_line_clear_detection_clear_2(self):
    processor = create_gameboy_view_processor_with("test/full-view/gameboy-full-view-tetris-2.png")
    playfield_processor = PlayfieldProcessor(processor.get_playfield(), image_is_tiled=True)
    playfield = playfield_processor.run()
    self.assertEqual(2, playfield.line_clear_count)
    self.assertTrue(playfield.is_line_clear())

  def test_playfield_non__clear_detection(self):
    processor = create_gameboy_view_processor_with("test/full-view/gameboy-full-view-non-tetris.png")
    playfield_processor = PlayfieldProcessor(processor.get_playfield(), image_is_tiled=True)
    playfield = playfield_processor.run()
    self.assertEqual(0, playfield.line_clear_count)
    self.assertFalse(playfield.is_line_clear())

  def test_playfield_processor_transition_detection(self):
    processor = create_gameboy_view_processor_with("test/full-view/gameboy-full-view-in-transition.png")
    playfield_processor = PlayfieldProcessor(processor.get_playfield(), image_is_tiled=True)
    playfield = playfield_processor.run()
    self.assertTrue(playfield.in_transition)

  def test_playfield_processor_transition_detection_2(self):
    processor = create_gameboy_view_processor_with("test/full-view/gameboy-full-view-in-transition-2.png")
    playfield_processor = PlayfieldProcessor(processor.get_playfield(), image_is_tiled=True)
    playfield = playfield_processor.run()
    self.assertTrue(playfield.in_transition)

  def test_playfield_processor_transition_detection_3(self):
    processor = create_gameboy_view_processor_with("test/full-view/gameboy-full-view-in-transition-3.png")
    playfield_processor = PlayfieldProcessor(processor.get_playfield(), image_is_tiled=True)
    playfield = playfield_processor.run()
    self.assertTrue(playfield.in_transition)

  def test_playfield_processor_transition_detection_4(self):
    processor = create_gameboy_view_processor_with("test/full-view/gameboy-full-view-in-transition-4.png")
    playfield_processor = PlayfieldProcessor(processor.get_playfield(), image_is_tiled=True)
    playfield = playfield_processor.run()
    self.assertTrue(playfield.in_transition)

  def test_playfield_processor_transition_detection_5(self):
    # This does not work as the difference is too small.
    # Another approach is needed here. This only happens
    # shortly after a line clear
    processor = create_gameboy_view_processor_with("test/full-view/gameboy-full-view-in-transition-problematic.png")
    playfield_processor = PlayfieldProcessor(processor.get_playfield(), image_is_tiled=True)
    playfield = playfield_processor.run()
    self.assertTrue(playfield.in_transition)

  def test_playfield_processor_not_transition_detection(self):
    processor = create_gameboy_view_processor_with("test/full-view/gameboy-full-view.png")
    playfield_processor = PlayfieldProcessor(processor.get_playfield(), image_is_tiled=True)
    playfield = playfield_processor.run()
    self.assertFalse(playfield.in_transition)

  def test_gameboy_view_processor(self):
      processor = create_gameboy_view_processor_with("test/full-view/gameboy-full-view.png")

      playfield = processor.get_playfield()
      self.assertEqual(playfield.shape[0], 18)
      self.assertEqual(playfield.shape[1], 10)

      preview = processor.get_preview()
      self.assertEqual(preview.shape[0], 4)
      self.assertEqual(preview.shape[1], 4)

      score = processor.get_score()
      self.assertEqual(score.shape[0], 1)
      self.assertEqual(score.shape[1], 6)

      lines = processor.get_lines()
      self.assertEqual(lines.shape[0], 1)
      self.assertEqual(lines.shape[1], 3)

  def full_image(self, image_path, test):
    image = np.array(Image.open(image_path).convert('RGBA'))
    playfield = PlayfieldProcessor(image)
    result = playfield.run().playfield_array
    self.performance(result, test)

  def performance(self, result, test):
    difference = result - test
    hits = result.copy()
    # set edge cases to no tile
    hits[hits > 11] = -99
    hits[hits > -99] = 1
    hits[hits == -99] = 0
    hits = hits - self.create_array_only_hits(test)
    false_negatives = hits.copy()
    false_negatives[hits == 1] = 0
    false_negatives[hits == -1] = 1
    performance = np.sum(false_negatives)
    self.assertEqual(0, performance, "Some false negatives")

    false_positives = hits.copy()
    false_positives[hits == -1] = 0
    performance = np.sum(false_positives)

    if (performance > 0):
      print(result)
      print(difference)

    self.assertEqual(0, performance, "Some false positives")

    arr = difference.copy()
    arr[arr > 0] = 1
    arr[arr < 0] = 1

    performance = np.sum(arr)
    if (performance > 0):
      print(arr)
    self.assertEqual(0, performance, "Some miscategorized minos")

  def test_full_view(self):
    image = get_image("test/full-view/gameboy-full-view.png")
    processor = GameboyViewProcessor(image)
    playfield_image = processor.get_playfield()
    playfield = PlayfieldProcessor(playfield_image, image_is_tiled=True).run(save_tiles=True).playfield_array
    self.performance(playfield, create_testing_array_full_view())

  def test_full_view_2(self):
    image = get_image("test/full-view/gameboy-full-view-2.png")
    processor = GameboyViewProcessor(image)
    playfield_image = processor.get_playfield()
    playfield = PlayfieldProcessor(playfield_image, image_is_tiled=True).run(save_tiles=True).playfield_array
    self.performance(playfield, create_testing_array_full_view_2())

  def test_second_scenario(self):
    self.full_image("test/scenario-2-high-res.png", create_testing_array_s2())

  def test_first_scenario(self):
    self.full_image("test/scenario-1-high-res.png", create_testing_array_s1())

  def create_array_only_hits(self, array):
    array = array.copy()
    array[array > -99] = 1
    array[array == -99] = 0
    return array