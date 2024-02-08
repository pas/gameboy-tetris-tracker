import cv2 as cv2
import tempfile

import yaml

class InterceptorCapturer:
  def __init__(self,  config, create_temp_dir=True):
    """
    This creates a temporary directory to store
    the images of the successful attempts to
    connect to a camera

    Reads camera from config yaml file
    e.g.

    interceptor_capturer:
      camera: 2
    """
    self.cap = None
    self.config = config

    self.create_temp_dir = create_temp_dir
    if(self.create_temp_dir):
      self.temp_dir = tempfile.TemporaryDirectory()

    self.set_camera()

  def set_camera(self):
    # TODO: Error handling!
    self.release()

    self.cap = cv2.VideoCapture(self.config.get_interceptor_camera_index())

  def release(self):
    if(self.cap != None):
      self.cap.release()

  def grab_image(self, enhancement=True):
    """
    This tries to fetch an image
    from the camera. Should it not
    be successful it tries multiple
    times. Should this not be successful
    this method throws an error

    :param enhancement:
    :return: grabed image from camera
    """
    ret = False
    tries = 0
    while not (ret or tries > 100):
      """
      It sometimes happens that no image can be fetched
      we just try again if this happens
      """
      ret, image = self.cap.read()
      tries += 1

    if not ret:
      raise RuntimeError("Could not fetch image from camera")

    if(enhancement):
      image = self._enhance(image)

    return image

  def _enhance(self, image):
    """
    The new version of the interceptor does not
    return a clean image. This enhances the image
    to make clean borders and have totally black
    and totally white pixels.
    Unsure what happens when blurring occurs...
    """

    image[(image >= 31) & (image <= 33)] = 0
    image[(image >= 95) & (image <= 97)] = 85
    image[(image >= 159) & (image <= 161)] = 170
    image[(image >= 223) & (image <= 225)] = 255
    return image

  def create_unique_name(self, values):
    return str(values[0]) + values[2]

  def get_image_path(self, values):
    return self.temp_dir.name + "\\" + self.create_unique_name(values) + ".png"

  def close(self):
    self.temp_dir.cleanup()



