import unittest

from test.helpers import create_gameboy_view_processor_with, get_number


class TestLinesProcessor(unittest.TestCase):
  def get_lines(self, processor, save_image=False):
    lines_image = processor.get_lines()
    lines = get_number(lines_image, save_image)
    return lines

  def test_lines_processor_with_gameboy_view_processor(self):
    processor = create_gameboy_view_processor_with("test/full-view/gameboy-full-view.png")

    lines = self.get_lines(processor)
    self.assertEqual(0, lines)

  def test_problematic_lines_with_gameboy_view_processor(self):
    # Currently not fixable
    processor = create_gameboy_view_processor_with("test/full-view/gameboy-full-view-problematic-lines.png")
    self.assertEqual(9, self.get_lines(processor))

