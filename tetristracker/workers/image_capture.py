import numpy as np

from tetristracker.capturer.capture_selection import CaptureSelection
from tetristracker.helpers.config import Config
from tetristracker.workers.get import Get


class ImageCapture(Get):
  def __init__(self):
    config = Config()
    self.previous = None

    # create capturer (this seems to have to be inside
    # the local thread or else mss doesn't work)
    capture_selection = CaptureSelection(config)
    capture_selection.select(config.get_capturer())

    capturer = capture_selection.get()

    self.capturer = capturer

  def get(self):
    image = self.capturer.grab_image()

    if(not self.previous is None):
      # We don't want to capture the exact same image twice...
      while(np.sum(self.previous - image) < 900000): # TODO: This number is stupid as it should be percentage of the image...
        image = self.capturer.grab_image()
    self.previous = image

    return image
