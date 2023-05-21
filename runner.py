import yaml
from tetristracker.game import Game
from tetristracker.capturer.mss_capturer import MSSCapturer
from tetristracker.plotter import Plotter


class Runner:
  def __init__(self, config_file="config.yml"):
    with open('config.yml', 'r') as config_file:
      self.configs = yaml.safe_load(config_file)
      bounding_box = self.configs["bounding_box"]
      self.capturer = MSSCapturer(bounding_box)
      self.plotter = Plotter()

  def run(self):
    game = Game(self.capturer, self.plotter)
    game.start()

if __name__ == "__main__":
  runner = Runner()
  runner.run()
