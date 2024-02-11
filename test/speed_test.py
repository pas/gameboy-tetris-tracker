import time
import unittest
from queue import Queue
from threading import Thread

from tetristracker.capturer.mss_capturer import MSSCapturer
from tetristracker.helpers.config import Config
from tetristracker.processor.playfield_processor import PlayfieldProcessor

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
