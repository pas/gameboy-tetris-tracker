import cv2


class ImageSaver():
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
