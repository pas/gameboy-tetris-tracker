import numpy as np
from PIL import Image
from mss import mss
from threading import Lock


class MSSCapturer:
  """
  This capturer expects a blak border that gets removed
  by the capturer itself.
  """
  def __init__(self, bounding_box):
    self.sct = mss()
    self.bounding_box = bounding_box

  def recalculate_border(self):
    pass

  def grab_image(self):
    # TODO: Check if this lock is actually needed. I think this is a remnant from older times...
    lock = Lock()
    lock.acquire()
    screenshot = self.sct.grab(self.bounding_box)
    lock.release()
    return np.array(Image.fromarray(np.array(screenshot)).convert('RGB'))

  def remove_border(self, image):
    return self.trim(image)

  def trim(self, image):
    result, self.top, self.bottom, self.left, self.right = self._trim(image, 0, 0, 0, 0)
    return result

  def _trim(self, frame, top, bottom, left, right):
    if frame.shape[0] == 0:
      return np.zeros((0, 0, 3))

    print(np.sum(frame[0]))
    print(frame[0])

    # crop top
    if not np.sum(frame[0]):
      return self._trim(frame[1:], top+1, bottom, left, right)
    # crop bottom
    elif not np.sum(frame[-1]):
      return self._trim(frame[:-1], top, bottom+1, left, right)
    # crop left
    elif not np.sum(frame[:, 0]):
      return self._trim(frame[:, 1:], top, bottom, left+1, right)
      # crop right
    elif not np.sum(frame[:, -1]):
      return self._trim(frame[:, :-1], top+1, bottom, left, right+1)

    return frame, top, bottom, left, right
