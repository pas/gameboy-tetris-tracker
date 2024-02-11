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

  def test_adding_up_gamescom(self):
    """
    Those are not actual tests...
    """
    plotter = PieceDistributionPlotter(file_name="piece-distribution-gamescom-4games", mode="gamescom ROM")
    # J Z O L T S I
    one = np.array([83, 85, 96, 70, 113, 92, 97])
    two = np.array([46, 47, 68, 46, 53, 54, 55])
    three = np.array([52, 57, 65, 37, 50, 53, 57])
    four = np.array([33, 34, 35, 30, 42, 46, 42])
    five = np.array([82, 76, 85, 45, 68, 94, 97])
    six = np.array([51, 46, 49, 31, 66, 45, 47])
    seven = np.array([35, 28, 33, 26, 31, 32, 37])

    dist = one + two + three + four + five + six + seven
    plotter.show_plot(None, None, dist, show_expected=True)


  def test_adding_up_orig(self):
    """
    Those are not actual tests...
    """
    plotter = PieceDistributionPlotter(file_name="piece-distribution-orig-l9-3games")
    # J Z O L T S I
    one = np.array([65, 52, 92, 43, 65, 77, 78])
    two = np.array([63, 49, 65, 37, 71, 71, 63])
    three = np.array([50, 50, 58, 53, 58, 69, 56])
    four = np.array([57, 55, 60, 62, 72, 74, 69])
    five = np.array([40, 34, 55, 34, 45, 56, 54])
    six = np.array([56, 49, 53, 47, 50, 49, 63])

    dist = one + two + three + four + five + six
    plotter.show_plot(None, None, dist, show_expected=True)

  def test_adding_up_sps(self):
    """
    Those are not actual tests...
    """
    plotter = PieceDistributionPlotter(file_name="piece-distribution-sps-l9-3games", mode="SPS")
    # J Z O L T S I
    one = np.array([32, 30, 17, 20, 32, 28, 25]) # 1213
    two = np.array([66, 62, 78, 49, 86, 77, 86]) # 2123
    three = np.array([71, 53, 71, 55, 67, 70, 75]) # 3119
    four = np.array([74, 53, 60, 49, 70, 64, 70]) # 4118
    five = np.array([53, 44, 48, 35, 47, 70, 61]) # 5933
    six = np.array([48, 56, 65, 42, 68, 67, 76]) # 6239

    dist = one + two + three + four + five + six
    plotter.show_plot(None, None, dist, show_expected=True)

