import cv2 as cv2
import tempfile

import numpy as np
import yaml

class OBSVirtualCamCapturer:

  def __init__(self, bounding_box, config, create_temp_dir=True):
    """
    This creates a temporary directory to store
    the images of the successful attempts to
    connect to a camera

    Reads camera from config yaml file
    e.g.

    obs_virtual_cam_capturer:
      camera: 2
    """
    self.cap = None
    self.cap = None
    self.config = config

    self.create_temp_dir = create_temp_dir
    if(self.create_temp_dir):
      self.temp_dir = tempfile.TemporaryDirectory()

    self.set_camera()

    self.bounding_box = bounding_box

  def set_camera(self):
    # TODO: Error handling!
    self.release()

    print("selected camera for obs:")
    print(self.config.get_obs_camera_index())
    print(self.config.get_obs_camera_api())
    self.cap = cv2.VideoCapture(self.config.get_obs_camera_index())
    self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

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

    reset_tries = 0
    ret = False
    while not (ret or reset_tries > 100):
      grab_tries = 0
      while not (ret or grab_tries > 100):
        """
        It sometimes happens that no image can be fetched
        we just try again if this happens
        """
        ret, image = self.cap.read()
        grab_tries += 1

      if not ret:
        # we try to release the camera
        # and then reconfigure again
        print("Could not read from camera. Resetting!")
        self.release()
        self.set_camera()
        reset_tries += 1

    if not ret:
      raise RuntimeError("---> Could not fetch image from camera <---")

    image = self.crop(image)

    if(enhancement):
      image = self._enhance(image)

    return image

  def crop(self, image):
    return image[self.bounding_box["top"]: self.bounding_box["top"] + self.bounding_box["height"] ,
           self.bounding_box["left"] : self.bounding_box["left"]  + self.bounding_box["width"]]


  def _enhance(self, image):
    """
    No enhancement
    """
    return image



