from tetristracker.capturer.capturer import Capturer


class VideofileCapturer (Capturer):
  def __init__(self, file_name):
    self.file_name = file_name

  def grab_image(self):
    pass