import time

class Timer:
  """
  You need to call start before wait_then_restart.
  """
  def __init__(self, delay=1000/62): # 60 images per second
    """
    Put in the delay in miliseconds
    """
    self.delay = delay

  def start(self):
    """
    Sets internal clock to 0
    """
    self.start_time = time.time() * 1000

  def time_passed(self):
    return time.time() * 1000 - self.start_time

  def wait_then_restart(self):
    """
    Stops processing (waits) until time of
    delay is over since last hitting
    #start. Immediately returns if
    time already passed.
    It does reset the clock to 0.
    Please be
    aware that this is always an
    approximation.
    """
    time_passed = self.time_passed()
    if (time_passed < self.delay):
      time.sleep((self.delay - time_passed) / 1000)
    self.start()