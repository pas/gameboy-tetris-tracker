import yaml

from tetristracker.game import Game
from tetristracker.plotter import Plotter


class Runner:
  def __init__(self, capturer):
      self.capturer = capturer
      self.plotter = Plotter()

  def run(self):
    game = Game(self.capturer, self.plotter)
    game.start()

if __name__ == "__main__":
  runner = Runner()
  runner.run()
