import unittest

from tetristracker.image.stats_image import StatsImage


class TestStatsView(unittest.TestCase):
  def test_stats_image(self):
    stat = StatsImage()
    stat.create_image([0, 1, 10, 200, 2, 5, 7])