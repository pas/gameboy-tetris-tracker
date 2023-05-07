from abc import ABC, abstractmethod
from mss import mss

class Capturer:
  @abstractmethod
  def grab_image(self):
    pass

class MSSCapturer:
  def __init__(self, bounding_box):
    self.sct = mss()
    self.bounding_box = bounding_box

  def grab_image(self):
    return self.sct.grab(self.bounding_box)

