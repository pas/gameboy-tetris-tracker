from abc import ABC, abstractmethod
from mss import mss
import cv2 as cv2
import numpy as np
from PIL import Image
from image_manipulator import convert_to_4bitgrey

class Capturer:
  @abstractmethod
  def grab_image(self):
    """
    Returns a RGB image
    """
    pass

class MSSCapturer:
  """
  This capturer expects a blak border that gets removed
  by the capturer itself.
  """
  def __init__(self, bounding_box):
    self.sct = mss()
    self.bounding_box = bounding_box

  def recalculate_border(self):
    pass

  def grab_image(self):
    return np.array(Image.fromarray(np.array(self.sct.grab(self.bounding_box))).convert('RGB'))

  def remove_border(self, image):
    return self.trim(image)

  def trim(self, image):
    result, self.top, self.bottom, self.left, self.right = self._trim(image, 0, 0, 0, 0)
    return result
    
  def _trim(self, frame, top, bottom, left, right):
    if frame.shape[0] == 0:
      return np.zeros((0, 0, 3))

    print(np.sum(frame[0]))
    print(frame[0])

    # crop top
    if not np.sum(frame[0]):
      return self._trim(frame[1:], top+1, bottom, left, right)
    # crop bottom
    elif not np.sum(frame[-1]):
      return self._trim(frame[:-1], top, bottom+1, left, right)
    # crop left
    elif not np.sum(frame[:, 0]):
      return self._trim(frame[:, 1:], top, bottom, left+1, right)
      # crop right
    elif not np.sum(frame[:, -1]):
      return self._trim(frame[:, :-1], top+1, bottom, left, right+1)

    return frame, top, bottom, left, right

class OCVCapturer:
  def __init__(self):
    print(cv2.__version__)
    #self.list_ports()
    #self.check_ports()

  def check_ports(self):
    # let's hope nobody uses more than five cameras...
    for index in range(0, 10):
      for api in [cv2.CAP_VFW, cv2.CAP_V4L, cv2.CAP_V4L2, cv2.CAP_FIREWIRE, cv2.CAP_FIREWARE, cv2.CAP_IEEE1394,
                  cv2.CAP_DC1394, cv2.CAP_CMU1394, cv2.CAP_QT, cv2.CAP_UNICAP, cv2.CAP_DSHOW,
                  cv2.CAP_PVAPI, cv2.CAP_OPENNI, cv2.CAP_OPENNI_ASUS, cv2.CAP_ANDROID, cv2.CAP_XIAPI,
                  cv2.CAP_AVFOUNDATION, cv2.CAP_GIGANETIX, cv2.CAP_MSMF, cv2.CAP_WINRT, cv2.CAP_INTELPERC,
                  cv2.CAP_OPENNI2, cv2.CAP_OPENNI2_ASUS, cv2.CAP_GPHOTO2, cv2.CAP_GSTREAMER, cv2.CAP_FFMPEG,
                  cv2.CAP_IMAGES, cv2.CAP_ARAVIS, cv2.CAP_INTEL_MFX,
                  cv2.CAP_XINE]:
        cap = cv2.VideoCapture(index, api)
        if not cap.isOpened():
          print("Cannot open camera")
        else:
          print(cap.getBackendName())
          try:
            ret, image = cap.read()
            cv2.imwrite("screenshots/test" + str(index) + "-" + str(api) + ".png", image)
          except:
            print("Could not grab image")

          cap.release()

  def list_ports(self):
    """
    Test the ports and returns a tuple with the available ports and the ones that are working.
    From: https://stackoverflow.com/a/62639343
    By: G M (CC-BY)
    """
    non_working_ports = []
    dev_port = 0
    working_ports = []
    available_ports = []
    while len(non_working_ports) < 6:  # if there are more than 5 non working ports stop the testing.
      camera = cv2.VideoCapture(dev_port)
      if not camera.isOpened():
        non_working_ports.append(dev_port)
        print("Port %s is not working." % dev_port)
      else:
        is_reading, img = camera.read()
        w = camera.get(3)
        h = camera.get(4)
        if is_reading:
          print("Port %s is working and reads images (%s x %s)" % (dev_port, h, w))
          working_ports.append(dev_port)
        else:
          print("Port %s for camera ( %s x %s) is present but does not reads." % (dev_port, h, w))
          available_ports.append(dev_port)
      dev_port += 1
    return available_ports, working_ports, non_working_ports

