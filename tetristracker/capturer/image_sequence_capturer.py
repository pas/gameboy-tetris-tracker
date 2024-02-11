import cv2

from tetristracker.capturer.capturer import Capturer
import os.path

class ImageSequenceCapturer(Capturer):
  def __init__(self, file_name : str, nr_of_images : int, start_nr=0,  file_ending="png"):
    self.file_name = file_name
    self.start_nr = start_nr
    self.nr_of_images = nr_of_images
    self.file_ending = file_ending

    self.current_nr = start_nr
    self.images_available = True

  def _get_path(self):
    return self.file_name + "-" + str(self.current_nr) + "." + self.file_ending
  def grab_image(self):
    if(self.nr_of_images+self.start_nr >= self.current_nr):
      image = cv2.imread(self._get_path())

      # current frame was consumed
      self.current_nr += 1

    return image

  def has_image(self):
    return self.current_nr <= self.nr_of_images+self.start_nr and os.path.isfile(self._get_path())
