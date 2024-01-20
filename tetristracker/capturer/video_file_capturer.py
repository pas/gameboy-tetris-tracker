from tetristracker.capturer.capturer import Capturer
import cv2 as cv


class VideoFileCapturer(Capturer):
  def __init__(self, file_name, bounding_box):
    self.file_name = file_name
    self.video = cv.VideoCapture(file_name)
    self.bounding_box = bounding_box

  def grab_image(self):
    if self.video.isOpened():
      ret, frame = self.video.read()
      # if frame is read correctly ret is True
      if not ret:
        print("Can't receive frame. Stream end?")

    return frame

  def release(self):
    self.video.release()
