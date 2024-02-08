import unittest

import numpy as np

from tetristracker.plotter.progress_plotter import ProgressPlotter
from tetristracker.plotter.piece_distribution_plotter import PieceDistributionPlotter


class TestStandardPlotter(unittest.TestCase):
  def test_perfect_score(self):
    plotter = ProgressPlotter()
    scores, lines = plotter.get_perfect_score_table()
    plotter.show_plot(scores, lines, None)
    self.assertTrue(scores[-1], 1401300)

  def test_worst_score(self):
    plotter = ProgressPlotter()
    scores, lines = plotter.get_worst_score_table()
    plotter.show_plot(scores, lines, None)
    self.assertTrue(len(scores), 300)

class TestPieceDistributionPlotter(unittest.TestCase):
  def test_creation(self):
    plotter = PieceDistributionPlotter()
    #       J  Z  O  L  T  S  I
    dist = [1, 3, 4, 5, 6, 9, 2]
    #plotter.show_plot(None, None, dist)

  def test_adding_up_orig(self):
    """
    Those are not actual tests...
    """
    plotter = PieceDistributionPlotter(file_name="piece-distribution-orig-l9-3games")
    # J Z O L T S I
    one = np.array([65, 52, 92, 43, 65, 77, 78])
    two = np.array([63, 49, 65, 37, 71, 71, 63])
    three = np.array([50, 50, 58, 53, 58, 69, 56])

    dist = one + two + three
    plotter.show_plot(None, None, dist)

  def test_adding_up_sps(self):
    """
    Those are not actual tests...
    """
    plotter = PieceDistributionPlotter(file_name="piece-distribution-sps-l9-3games")
    # J Z O L T S I
    one = np.array([32, 30, 17, 20, 32, 28, 25]) # 1213
    two = np.array([66, 62, 78, 49, 86, 77, 86]) # 2123
    three = np.array([71, 53, 71, 55, 67, 70, 75]) # 3119
    dist = one + two + three
    plotter.show_plot(None, None, dist)

