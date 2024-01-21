from tetristracker.tracker.larger_or_equal_tracker import LargerOrEqualTracker


class LinesTracker(LargerOrEqualTracker):
  # This exists just to make the code clearer
  def track(self, lines):
    super().track(lines)


