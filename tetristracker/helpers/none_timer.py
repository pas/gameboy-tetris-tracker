class NoneTimer():
  """
  This timer does nothing.
  """
  def __init__(self, delay=0):
    pass

  def start(self):
    pass

  def time_passed(self):
    return 0

  def wait_then_restart(self):
    pass