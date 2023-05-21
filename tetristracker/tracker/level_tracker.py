from tetristracker.tracker.larger_or_equal_tracker import LargerOrEqualTracker


class LevelTracker(LargerOrEqualTracker):
  # This is just to make the code clear
  def track(self, level):
    super().track(level)
