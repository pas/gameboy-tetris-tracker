import time
import unittest
from queue import Queue
from threading import Thread

from tetristracker.capturer.image_sequence_capturer import ImageSequenceCapturer
from tetristracker.capturer.mss_capturer import MSSCapturer
from tetristracker.commasv.writer import Writer
from tetristracker.game import Game, Round
from tetristracker.helpers.config import Config
from tetristracker.processor.gameboy_view_processor import GameboyViewProcessor
from tetristracker.processor.playfield_processor import PlayfieldProcessor
from tetristracker.runner import Runner

q = Queue()
def worker():
  while True:
    image = q.get()
    processor = PlayfieldProcessor(image)
    q.task_done()



class TestSpeed(unittest.TestCase):
  def get_mss_capturer(self):
    config = Config()
    return MSSCapturer(config.get_screen_bounding_box())

  """
  Trying to optimize speed:
  Goal: at least 30 images per second
  """
  def test_mss_speed(self):
    mssCapturer = self.get_mss_capturer()

    iterations = 120 # 4 seconds

    start = time.perf_counter()
    for _ in range(0, iterations):
      mssCapturer.grab_image()
    end = time.perf_counter()
    passed_time = end-start
    print("Needed " + str(passed_time) + " seconds for " + str(iterations) + " images.")
    self.assertTrue(passed_time < 4.0)

  def test_mss_speed_with_processor(self):
    mss_capturer = self.get_mss_capturer()

    iterations = 120  # 4 seconds

    start = time.perf_counter()
    for _ in range(0, iterations):
      image = mss_capturer.grab_image()
      processor = PlayfieldProcessor(image)

    end = time.perf_counter()
    passed_time = end - start
    print("Needed " + str(passed_time) + " seconds for " + str(iterations) + " images.")
    self.assertTrue(passed_time < 4.0)

  def test_mss_speed_with_queues(self):
    t = Thread(target=worker, daemon=True)
    t.start()

    mss_capturer = self.get_mss_capturer()

    iterations = 120  # 4 seconds

    start = time.perf_counter()
    for _ in range(0, iterations):
      image = mss_capturer.grab_image()
      q.put(image)

    end = time.perf_counter()
    passed_time = end - start
    print("Needed " + str(passed_time) + " seconds for " + str(iterations) + " images.")
    self.assertTrue(passed_time < 4.0)

    q.join()

  class GameMock():
    def __init__(self, images: Queue):
      self.images = images

    def get_gameboy_view_processor(self):
      return self.images.get()

    def is_running(self, processor):
      return not self.images.empty()

    def force_stop(self):
      return False

  class MockPlotter:
    def show_plot(self, x, y, z):
      pass

  class MockWriter(Writer):
    def write(self, score: int, lines: int, level: int, preview: int, tetromino_in_play: int, spawned: bool, playfield):
      pass

    def restart(self):
      pass

  class MockSaver():
    def save(self, processor):
      pass

  def test_run_speed(self):
    iterations = 60
    capturer = ImageSequenceCapturer("test/sequence/full-game-with-transition/retrieved",
                                     nr_of_images=iterations,
                                     start_nr=143)

    images = Queue()
    while(capturer.has_image()):
      images.put(GameboyViewProcessor(image=capturer.grab_image()))

    game = TestSpeed.GameMock(images)
    writer = TestSpeed.MockWriter()
    plotter = TestSpeed.MockPlotter()
    saver = TestSpeed.MockSaver()

    start = time.perf_counter()
    round = Round(game, saver, plotter, writer)
    processor = images.get()
    round.start(processor)
    end = time.perf_counter()

    passed_time = end - start
    print("Needed " + str(passed_time) + " seconds for " + str(iterations) + " images.")
    print(str(iterations/passed_time) + " images for 1 second")
    self.assertTrue(passed_time < 4.0)

  def test_playfield_processing_speed(self):
    """
    This is the offending part which is very
    slow. I'd like to have this at a
    way higher speed.
    Currently at 24 images per second
    Goal: 60 images per second
    :return:
    """
    iterations = 60
    capturer = ImageSequenceCapturer("test/sequence/full-game-with-transition/retrieved",
                                     nr_of_images=iterations,
                                     start_nr=143)

    images = Queue()
    while (capturer.has_image()):
      images.put(GameboyViewProcessor(image=capturer.grab_image()))

    start = time.perf_counter()
    for _ in range(0, iterations):
      processor = images.get()
      playfield_image = processor.get_playfield()
      playfield_processor = PlayfieldProcessor(playfield_image, image_is_tiled=True)
      playfield_processor.run(return_on_transition=True)

    end = time.perf_counter()

    passed_time = end - start
    print("Needed " + str(passed_time) + " seconds for " + str(iterations) + " images.")
    print(str(iterations / passed_time) + " images for 1 second")
    self.assertTrue(passed_time < 2.0)
