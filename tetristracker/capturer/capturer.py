from abc import abstractmethod


class Capturer:
  @abstractmethod
  def grab_image(self):
    """
    Returns a RGB image
    """
    pass