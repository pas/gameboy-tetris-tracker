from abc import ABC
import cv2 as cv2
import tempfile

import yaml

class CameraDetector:
  """
  Detects all available cameras. Stores
  image of each camera in temp folder.

  Introduces functionalities like checking
  for available cameras and retrieving
  images from current camera
  """

  def __init__(self, create_temp_dir=True):
    """
    This creates a temporary directory to store
    the images of the successful attempts to
    connect to a camera.
    """
    self.cap = None

    self.create_temp_dir = create_temp_dir
    if (self.create_temp_dir):
      self.temp_dir = tempfile.TemporaryDirectory()

    # Looking for available cameras
    self.working_values = self.check_ports()

  def check_ports(self):
    """
    Returns all working values with
    1) camera index
    2) API value
    3) API Name
    :return:
    """
    working_values = []
    # let's hope nobody uses more than five cameras...
    for index in range(0, 5):
      for api in self._small_api():
        values = []
        values.append(index)
        values.append(api)
        cap = cv2.VideoCapture(index, api)
        if cap.isOpened():
          values.append(cap.getBackendName())
          try:
            ret, image = cap.read()
            if (ret):
              if (self.create_temp_dir):
                # The image is resized here as it is only intended to be
                # used as button
                dim = (200, 200)
                resized = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
                cv2.imwrite(self.get_image_path(values), resized)
              working_values.append(values)
            else:
              raise Exception("No image received in cap.read")
          except Exception as ex:
            print("Could not grab image")
            print(ex)

          cap.release()

    return working_values

  def _small_api(self):
    """
    Only apis that where somehow important
    during my testing and on my system.
    """
    return [cv2.CAP_DSHOW, cv2.CAP_MSMF]

  def create_unique_name(self, values):
    return str(values[0]) + values[2]

  def get_image_path(self, values):
    return self.temp_dir.name + "\\" + self.create_unique_name(values) + ".png"

  def close(self):
    self.temp_dir.cleanup()

  def _full_api(self):
    """
    This is only here as reference. It is not used.
    """
    return [cv2.CAP_VFW, cv2.CAP_V4L, cv2.CAP_V4L2, cv2.CAP_FIREWIRE, cv2.CAP_FIREWARE, cv2.CAP_IEEE1394,
            cv2.CAP_DC1394, cv2.CAP_CMU1394, cv2.CAP_QT, cv2.CAP_UNICAP, cv2.CAP_DSHOW,
            cv2.CAP_PVAPI, cv2.CAP_OPENNI, cv2.CAP_OPENNI_ASUS, cv2.CAP_ANDROID, cv2.CAP_XIAPI,
            cv2.CAP_AVFOUNDATION, cv2.CAP_GIGANETIX, cv2.CAP_MSMF, cv2.CAP_WINRT, cv2.CAP_INTELPERC,
            cv2.CAP_OPENNI2, cv2.CAP_OPENNI2_ASUS, cv2.CAP_GPHOTO2, cv2.CAP_GSTREAMER, cv2.CAP_FFMPEG,
            cv2.CAP_IMAGES, cv2.CAP_ARAVIS, cv2.CAP_INTEL_MFX,
            cv2.CAP_XINE]

  def list_ports(self):
    """
    Test the ports and returns a tuple with the available ports and the ones that are working.
    From: https://stackoverflow.com/a/62639343
    This is currently unused
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
