class SimpleTracker:
  def __init__(self):
    self.current = -1
    self.previous = -1

  def track(self, value):
    self.previous = self.current
    self.current = value
