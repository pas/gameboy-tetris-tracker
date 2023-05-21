from tetristracker.tracker.larger_or_equal_tracker import LargerOrEqualTracker


class ScoreTracker(LargerOrEqualTracker):
  # This is just to make the code clear
  def track(self, score):
    super().track(score)
