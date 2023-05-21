from tetristracker.tracker.tracker import Tracker


class LargerOrEqualTracker(Tracker):
  def track(self, value):
    """
    The check for >= is a little bit of false value prevention (not a good one though...)
    """
    if(value != None):
      if(value < self.accepted):
        value = -1
    else:
      value = -1

    super().track(value)