import unittest

from test.helpers import create_gameboy_view_processor_with, get_score


class TestScoreProcessor(unittest.TestCase):
  def test_score_processor_from_gameboy_view_processor_39(self):
    processor = create_gameboy_view_processor_with("test/full-view/gameboy-full-view.png")
    score = get_score(processor)
    self.assertEqual(39, score)

  def test_score_processor_with_gameboy_view_processor_99(self):
    processor = create_gameboy_view_processor_with("test/full-view/gameboy-full-view-problematic-score.png")
    score = get_score(processor)
    self.assertEqual(99, score)

  def test_score_processor_with_gameboy_view_processor_151753_with_image_from_ocv_capturer(self):
    processor = create_gameboy_view_processor_with("test/full-view/gameboy-full-view-problematic-score-ocv-capturer.png")
    score = get_score(processor)
    self.assertEqual(151753, score)

  def test_score_processor_with_gameboy_view_processor_in_transition_with_image_from_ocv_capturer(self):
    # This is not solved and should fail.
    processor = create_gameboy_view_processor_with("test/full-view/gameboy-full-view-problematic-score-in-transition-ocv-capturer.png")
    score = get_score(processor)
    self.assertEqual(151753, score, "This test is currently failing. Need to check if this matters.")
