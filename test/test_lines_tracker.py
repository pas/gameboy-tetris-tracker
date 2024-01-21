import unittest

from tetristracker.tracker.lines_tracker import LinesTracker

class TestLinesTracker(unittest.TestCase):
  def test__after_init(self):
    tracker = LinesTracker()
    self.assertTrue(tracker.is_empty())

  def test_first_lines(self):
    tracker = LinesTracker()
    tracker.track(1)
    self.assertEqual(tracker.accepted, 1)
    self.assertFalse(tracker.is_empty())
    self.assertFalse(tracker.has_changed())
    self.assertTrue(tracker.is_accepted())

  def test_not_accepted_first_lines(self):
    tracker = LinesTracker()
    tracker.track(None)
    # TODO: This feels like an odd behaviour as a -1 does not get accepted ever
    # TODO: I feel like this should be None
    self.assertEqual(tracker.accepted, -1)
    self.assertFalse(tracker.is_empty())
    self.assertFalse(tracker.has_changed())
    self.assertFalse(tracker.is_accepted())

  def test_none_value_second_lines(self):
    tracker = LinesTracker()
    tracker.track(1)
    tracker.track(None)
    self.assertEqual(tracker.accepted, 1)
    self.assertFalse(tracker.is_empty())
    # TODO: Is this what we would expect?
    self.assertTrue(tracker.has_changed())
    self.assertFalse(tracker.is_accepted())

  def test_smaller_value_second_lines(self):
    tracker = LinesTracker()
    tracker.track(4)
    tracker.track(2)
    # The four is the last accepted as 2 gets rejected
    self.assertEqual(tracker.accepted, 4)
    self.assertFalse(tracker.is_empty())
    # TODO: Is this what we would expect?
    self.assertTrue(tracker.has_changed())
    self.assertFalse(tracker.is_accepted())

  def test_equal_value_second_lines(self):
    tracker = LinesTracker()
    tracker.track(4)
    tracker.track(4)
    # The four is the last accepted as 2 gets rejected
    self.assertEqual(tracker.accepted, 4)
    self.assertFalse(tracker.is_empty())
    self.assertFalse(tracker.has_changed())
    self.assertTrue(tracker.is_accepted())

  def test_two_valid_lines(self):
    tracker = LinesTracker()
    tracker.track(1)
    tracker.track(2)
    self.assertEqual(tracker.accepted, 2)
    self.assertFalse(tracker.is_empty())
    self.assertTrue(tracker.has_changed())
    self.assertTrue(tracker.is_accepted())

  def test_two_smaller_values_second_and_third_lines(self):
    tracker = LinesTracker()
    tracker.track(4)
    tracker.track(2)
    tracker.track(2)
    # The four is the last accepted as the two 2 get rejected
    self.assertEqual(tracker.accepted, 4)
    self.assertFalse(tracker.is_empty())
    # TODO: Is this expected behaviour?
    # This is because the last two values were stored
    # as -1
    self.assertFalse(tracker.has_changed())
    self.assertFalse(tracker.is_accepted())

  def test_larger_value_after_second_lines_was_not_accepted(self):
    tracker = LinesTracker()
    tracker.track(4)
    tracker.track(2)
    tracker.track(6)

    self.assertEqual(tracker.accepted, 6)
    self.assertFalse(tracker.is_empty())
    self.assertTrue(tracker.has_changed())
    self.assertTrue(tracker.is_accepted())

  def test_lines_difference_only_no_value_tracked(self):
    tracker = LinesTracker()
    # TODO: 0 better value?
    self.assertIsNone(tracker.difference())

  def test_lines_difference_only_one_value_tracked(self):
    tracker = LinesTracker()
    tracker.track(1)
    self.assertEqual(1, tracker.difference())

  def test_lines_difference_only_one_invalid_value_tracked(self):
    tracker = LinesTracker()
    tracker.track(None)
    self.assertIsNone(tracker.difference())

  def test_lines_difference_two_valid_values_tracker(self):
    tracker = LinesTracker()
    tracker.track(0)
    tracker.track(4)
    self.assertEqual(4, tracker.difference())

  def test_lines_difference_two_valid_values_tracker_with_invalid_between(self):
    tracker = LinesTracker()
    tracker.track(0)
    tracker.track(None)
    tracker.track(4)
    self.assertEqual(4, tracker.difference())
