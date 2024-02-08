from tetristracker.capturer.capturer import Capturer
import cv2 as cv
import numpy as np

class VideoFileCapturer(Capturer):
  def __init__(self, file_name, bounding_box):
    self.file_name = file_name
    self.video = cv.VideoCapture(file_name)
    self.bounding_box = bounding_box
    self.current_frame = None
    self.frames_available = False

  def grab_image(self):
    if self.video.isOpened():
      if(self.current_frame is None):
        self.frames_available, self.current_frame = self.video.read()

      # if frame is read correctly ret is True
      if not self.frames_available:
        raise EOFError()

      frame = np.array(self.current_frame)
      # current frame was consumed
      self.current_frame = None

      frame = frame[self.bounding_box["top"]:self.bounding_box["top"]+self.bounding_box["height"],
              self.bounding_box["left"]:self.bounding_box["left"]+self.bounding_box["width"]]

    return frame

  def has_image(self):
    if self.video.isOpened():
      if self.current_frame is None:
        self.frames_available, self.current_frame = self.video.read()
      return self.frames_available
    else:
      return False

  def release(self):
    self.video.release()
