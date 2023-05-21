import unittest

from tetristracker.plotter import Plotter


class TestPlotter(unittest.TestCase):
  def test_perfect_score(self):
    plotter = Plotter()
    scores, lines = plotter.get_perfect_score_table()
    plotter.show_plot(scores, lines)
    self.assertTrue(scores[-1], 1401300);

  def test_worst_score(self):
    plotter = Plotter()
    scores, lines = plotter.get_worst_score_table()
    plotter.show_plot(scores, lines)
    self.assertTrue(len(scores), 300);