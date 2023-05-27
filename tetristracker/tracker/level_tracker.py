from tetristracker.tracker.larger_or_equal_tracker import LargerOrEqualTracker


class LevelTracker(LargerOrEqualTracker):
  def track(self, level, is_heart):
    self.is_heart = is_heart
    super().track(level)
