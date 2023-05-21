import unittest

from test.helpers import get_number, create_gameboy_view_processor_with


class TestLevelProcessor(unittest.TestCase):
  def get_level(self, processor):
    level_image = processor.get_level()
    level = get_number(level_image)
    return level
  def test_level_processor_with_gameboy_view_processor(self):
    processor = create_gameboy_view_processor_with("test/full-view/gameboy-full-view.png")

    level = self.get_level(processor)
    self.assertEqual(0, level)

  def test_problematic_level_with_gameboy_view_processor(self):
    processor = create_gameboy_view_processor_with("test/full-view/gameboy-full-view-problematic-score.png")

    level = self.get_level(processor)
    self.assertEqual(9, level)