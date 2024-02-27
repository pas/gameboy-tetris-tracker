import numpy as np

from tetristracker.workers.get.get import Get


class ImageCapture(Get):
  def __init__(self, capturer):
    self.previous = None
    self.capturer = capturer

  def get(self):
    image = self.capturer.grab_image()

    if(not self.previous is None):
      # We don't want to capture the exact same image twice...
      while(np.sum(self.previous - image) < 900000): # TODO: This number is stupid as it should be percentage of the image...
        image = self.capturer.grab_image()
    self.previous = image

    return image
