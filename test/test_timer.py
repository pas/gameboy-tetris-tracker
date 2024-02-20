import time
import unittest

from tetristracker.helpers.none_timer import NoneTimer
from tetristracker.helpers.timer import Timer


class TimerTest(unittest.TestCase):
  def test_timer_60(self):
    timer = Timer(delay=1000/60)

    timer.start()
    start = time.perf_counter()
    for i in range(0, 60):
        timer.wait_then_restart()

    end = time.perf_counter()

    passed = end-start

    self.assertAlmostEqual(passed, 1, delta=0.03)
  def test_timer_30(self):
    timer = Timer(delay=1000 / 30)

    timer.start()
    start = time.perf_counter()
    for i in range(0, 30):
        timer.wait_then_restart()

    end = time.perf_counter()

    passed = end - start

    self.assertAlmostEqual(passed, 1, delta=0.03)

  def test_timer_none(self):
    timer = NoneTimer(delay=1000 / 30)

    timer.start()
    start = time.perf_counter()
    for i in range(0, 30):
        timer.wait_then_restart()

    end = time.perf_counter()

    passed = end - start

    self.assertAlmostEqual(passed, 0, delta=0.00001)