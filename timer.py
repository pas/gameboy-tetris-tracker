import time

class Timer:
  def __init__(self, delay=50):
    """
    Put in the delay in miliseconds
    """
    self.delay = 50

  def start(self):
    """
    Sets internal clock to 0
    """
    self.start_time = time.time() * 1000

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
    time_passed = time.time() * 1000 - self.start_time
    if (time_passed < 50):
      time.sleep((self.delay - time_passed) / 1000)
    self.start()