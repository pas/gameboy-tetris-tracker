from abc import ABC, abstractmethod

import cv2

class Saver(ABC):
  @abstractmethod
  def save(self):
    pass

class ImageSaver(Saver):
  """
  Saves image with ascending numbers
  """
  def __init__(self, path, name):
    self.count = 1
    self.path = path
    self.name = name

  def save(self, image):
    cv2.imwrite(self.path + self.name + "-" + str(self.count) + ".png", image)
    self.count += 1

class NullSaver(Saver):
  """
  This simple does not save
  any image and passes
  everything into the void
  """
  def __init__(self):
    pass

  def save(self, image):
    pass
