import unittest
from unittest.mock import Mock, patch

from tetristracker.workers import workers


class TestFullScale(unittest.TestCase):

  @patch('tetristracker.workers.workers.Looper')
  def test_capture_worker(self, MockLooper):
    """
    We only test if the looper starts
    """
    instance = MockLooper.return_value
    instance.start.return_value = None
    queue = Mock()
    workers.capture(queue)

    self.assertTrue(instance.start.called)
    self.assertFalse(queue.called)