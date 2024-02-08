from abc import abstractmethod


class Capturer:
  @abstractmethod
  def grab_image(self):
    """
    Returns a RGB image
    """
    pass

  def has_image(self):
    """
    Can be overwritten for capturers
    that provide a limited
    number of images (e.g. video capturer)
    """
    return True
