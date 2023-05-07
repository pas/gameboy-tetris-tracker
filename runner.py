import numpy as np
from mss import mss
import time
import matplotlib.pyplot as plt
from csvfile import CSVWriter
import yaml
import calculations
from play_sounds import play_file
import pathlib
from playfield_processor import PlayfieldProcessor, Playfield
from preview_processor import PreviewProcessor
from gameboy_view_processor import GameboyViewProcessor
from number_processor import NumberProcessor
from gameboy_image import GameboyImage
from image_saver import ImageSaver
from score_tracker import ScoreTracker, LinesTracker, PreviewTracker, PlayfieldTracker
from capturer import MSSCapturer
import cv2

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

  def preview(self, processor):
    """
    Returns -1 if results are ambigous
    """
    preview_image = processor.get_preview()
    preview_processor = PreviewProcessor(preview_image, image_is_tiled=True)
    result = preview_processor.run()
    if(preview_processor.ambigous):
      result = -1
    return result

  def playfield(self, processor):
    playfield_image = processor.get_playfield()
    playfield_processor = PlayfieldProcessor(playfield_image, image_is_tiled=True)
    return playfield_processor.run()

  def numbers(self, number_image):
    number_image = GameboyImage(number_image, number_image.shape[0], number_image.shape[1],
                               number_image.shape[2], number_image.shape[3], is_tiled=True)
    number_image.untile()
    number_processor = NumberProcessor(number_image.image)
    return number_processor.get_number()

  def score(self, processor):
    score_image = processor.get_score()
    return self.numbers(score_image)

  def lines(self, processor):
    lines_image = processor.get_lines()
    return self.numbers(lines_image)

  def level(self, processor):
    level_image = processor.get_level()
    return self.numbers(level_image)

  def is_break(self, processor):
    # this is a brittle hack. We just hope
    # that not another combination of
    # minos and whites return the same result
    continue_image = processor.get_continue()
    break_as_number = self.numbers(continue_image)
    return break_as_number == 71006

  def is_running(self, processor):
    """
    If the left top image is more or less
    black, then the game shows is in
    play state.
    """
    tile = processor.get_top_left_tile()
    return tile.is_black()

  def get_gameboy_view_processor(self):
    image = self.capturer.grab_image()
    cv2.imwrite('screenshots/current.png', np.array(image))
    return GameboyViewProcessor(image)

  def new_game(self):
    score_tracker = ScoreTracker()
    lines_tracker = LinesTracker()
    preview_tracker = PreviewTracker()
    playfield_tracker = PlayfieldTracker()
    playfield_tracker.track(Playfield.empty())

    saver = ImageSaver("test/debug/", "running")
    processor = self.get_gameboy_view_processor()
    saver.save(processor.original_image)

    while self.is_running(processor):  # Something like not processor.get_top_left_tile().is_black()
      processor = self.get_gameboy_view_processor()
      saver.save(processor.original_image)

      # Don't do anything user pressed break
      if self.is_break(processor):
        continue

      score_tracker.track(self.score(processor))
      lines_tracker.track(self.lines(processor))
      preview_tracker.track(self.preview(processor))
      playfield_tracker.track(self.playfield(processor))

      print("Score: " + str(score_tracker.last()) + " Lines: " + str(lines_tracker.last()))

      self.csv_file.write(score_tracker.last(), lines_tracker.last(), preview_tracker.last(), playfield_tracker.current.playfield_array)

      time.sleep(0.05)

  def run(self):
    while True:
      processor = self.get_gameboy_view_processor()
      if(self.is_running(processor)):
        self.csv_file = CSVWriter()
        self.new_game()

if __name__ == "__main__":
  runner = Runner()
  runner.run()
