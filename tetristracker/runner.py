import yaml

from tetristracker.game import Game


class Runner:
  def __init__(self, capturer, writer, plotter, shift_score=False):
      self.capturer = capturer
      self.plotter = plotter
      self.writer = writer
      self.shift_score = shift_score

  def run(self):
    game = Game(self.capturer, self.plotter, self.writer, shift_score=self.shift_score)
    game.start()

if __name__ == "__main__":
  runner = Runner()
  runner.run()
