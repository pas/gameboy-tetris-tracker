import unittest
from abc import ABC

import cv2

from test.helpers import create_gameboy_view_processor_with
from tetristracker.capturer.video_file_capturer import VideoFileCapturer
from tetristracker.storage.writer import Writer
from tetristracker.game import Game
from tetristracker.image.gameboy_image import GameboyImage
from tetristracker.processor.gameboy_view_processor import GameboyViewProcessor
from tetristracker.runner import Runner


class MockPlotter:
  def show_plot(self, x, y, z):
    pass

class MockWriter(Writer):
  def __init__(self, score_progression, test):
    self.score_progression = score_progression
    self.index = 0
    self.test = test
  def write(self, score : int, lines : int, level : int, preview : int, tetromino_in_play : int, spawned : bool, playfield):
    print(".", end='')

    if score == self.score_progression[self.index] or - 1:
      return

    self.index += 1

    if score == self.score_progression[self.index]:
      return

    print("Score: " + str(score))
    print("Lines: " + str(lines))
    print("level: " + str(level))
    print("preview: " + str(preview))

    self.test.fail()

  def restart(self):
    pass


class TestFullScale(unittest.TestCase):
  def tst_full_scale_video(self):
    """
    Does a full scale test along a video
    file. Not finished yet!
    """

    file_name = "test/video/video-test-full-68.mkv"
    score_progression = [0, 7, 17, 26, 40, 47, 52, 57, 61, 64, 68]
    tetromino_progression = ["TTSILSLTOLZZJZLISSOOSOT"]
    bounding_box =  { "height": 467, "left": 73, "top": 127, "width": 518}
    capturer = VideoFileCapturer(file_name, bounding_box)

    mock_plotter = MockPlotter()

    writer = MockWriter(score_progression, self)

    runner = Runner(capturer=capturer, plotter=mock_plotter, writer=writer)
    runner.run()

    capturer.release()

