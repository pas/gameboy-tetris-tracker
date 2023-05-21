from tetristracker.tracker.larger_or_equal_tracker import LargerOrEqualTracker


class LinesTracker(LargerOrEqualTracker):
  # This is just to make the code clear
  def track(self, lines):
    super().track(lines)
