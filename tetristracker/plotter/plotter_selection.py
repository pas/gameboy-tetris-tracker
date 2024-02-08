from tetristracker.helpers.config import Config
from tetristracker.plotter.piece_distribution_plotter import PieceDistributionPlotter
from tetristracker.plotter.progress_plotter import ProgressPlotter

class PlotterSelection:
  def __init__(self, config : Config):
    self.plotter = None
    self.name = ""
    self.config = config

  def get(self):
    return self.plotter

  def select(self, name):
    if(name == "piece_distribution"):
      self.select_piece_distribution()
    if(name == "progress"):
      self.select_progress()

  def select_piece_distribution(self):
    self.name = "piece_distribution"
    self.plotter = PieceDistributionPlotter()

  def select_progress(self):
    self.name = "progress"
    self.plotter = ProgressPlotter()