import numpy as np
from PIL import Image
from mss import mss

from tetristracker.capturer.capturer import Capturer
from tetristracker.helpers.none_timer import NoneTimer
from tetristracker.helpers.timer import Timer


class MSSCapturer(Capturer):
  def __init__(self, bounding_box, images_per_second=None):
    self.sct = mss()
    self.bounding_box = bounding_box

    if(not images_per_second is None):
      self.images_per_second = images_per_second
      self.timer = Timer(delay=1000/self.images_per_second-1.5) # it is no exactly precise so we wait a little less time then we should
    else:
      self.images_per_second = None
      self.timer = NoneTimer()
    self.timer.start()

  def grab_image(self):
    self.timer.wait_then_restart()
    screenshot = self.sct.grab(self.bounding_box)
    # TODO: Maybe better to just remove a grey image as GB Tetris is always in greyscale
    return np.array(Image.fromarray(np.array(screenshot)).convert('RGB'))
