import timeit

import numpy as np
from mss import mss
import time
import matplotlib.pyplot as plt
from csvfile import CSVWriter
import yaml
import calculations
from game import Game
from capturer import MSSCapturer

class Runner:
  def __init__(self, config_file="config.yml"):
    with open('config.yml', 'r') as config_file:
      self.configs = yaml.safe_load(config_file)
      self.bounding_box = self.configs["bounding_box"]
      self.capturer = MSSCapturer(self.bounding_box)
    self.csv_file = CSVWriter()

  def add_slope(self, slope, ax):
    x_min, x_max = ax.get_xlim()
    y_min, y_max = 0, slope * (x_max - x_min)
    ax.plot([x_min, x_max], [y_min, y_max])
    ax.set_xlim([x_min, x_max])

  def get_limits(self, current_max_score, current_max_lines):
    score = 1000

    # the uglier the better...
    if current_max_score > 1000:
      score = 10000
    if current_max_score > 10000:
      score = 100000
    if current_max_score > 100000:
      score = 500000
    if current_max_score > 500000:
      score = 999999

    lines = 10
    if current_max_lines > 10:
      lines = 50
    if current_max_lines > 50:
      lines = 100
    if current_max_lines > 100:
      lines = 150
    if current_max_lines > 150:
      lines = 200
    if current_max_lines > 200:
      lines = 250
    if current_max_lines > 250:
      lines = 300

    return score, lines

  def show_plot(self, scores, lines):
    if(len(scores) > 3):
      fig, ax = plt.subplots()
      ax.scatter(lines, scores)
      top, right = self.get_limits(scores[len(scores)-1], lines[len(lines)-1])
      ax.set_xlim(left=0, right=right)
      ax.set_ylim(bottom=0, top=top)
      slope = calculations.get_slope(lines, scores)
      self.add_slope(slope, ax)

      fig.savefig(r'plots/test.png')
      plt.close(fig)


  def run(self):
    """
    while True:
      processor = self.get_gameboy_view_processor()
      if(self.is_running(processor)):
        self.csv_file = CSVWriter()
        self.new_game()
    """
    game = Game(self.capturer)
    game.start()

if __name__ == "__main__":
  runner = Runner()
  runner.run()
