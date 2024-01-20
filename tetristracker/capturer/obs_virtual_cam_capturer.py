import cv2 as cv2
import tempfile

import yaml

class OBSVirtualCamCapturer:

  def __init__(self, bounding_box, create_temp_dir=True, ):
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

    self.create_temp_dir = create_temp_dir
    if self.create_temp_dir:
      self.temp_dir = tempfile.TemporaryDirectory()

    self.working_values = self.check_ports()

    with open('config.yml', 'r') as file:
      self.configs = yaml.safe_load(file)
    self.current_camera = self.configs['obs_virtual_cam_capturer']['camera']

    self.set_camera()

    self.bounding_box = bounding_box


  def set_camera(self):
    self.release()

    if self.current_camera < len(self.working_values):
      values = self.working_values[self.current_camera]
      self.cap = cv2.VideoCapture(values[0], values[1])
    else:
      print("Couldn't get any camera!")

  def next_camera(self):
    if self.current_camera < len(self.working_values):
      self.current_camera += 1
      self.set_camera()

  def store_camera(self):
    with open('config.yml', 'r') as file:
      self.configs = yaml.safe_load(file)

    self.configs['ocv_capturer']['camera'] = self.current_camera

    with open('config.yml', 'w') as file:
      yaml.dump(self.configs, file)

  def previous_camera(self):
    if(self.current_camera > 0):
      self.current_camera -= 1
      self.set_camera()

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
    return a clean black and white image. It is
    slightly greyish.

    This enhances the image
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

  def _full_api(self):
    return [cv2.CAP_VFW, cv2.CAP_V4L, cv2.CAP_V4L2, cv2.CAP_FIREWIRE, cv2.CAP_FIREWARE, cv2.CAP_IEEE1394,
                  cv2.CAP_DC1394, cv2.CAP_CMU1394, cv2.CAP_QT, cv2.CAP_UNICAP, cv2.CAP_DSHOW,
                  cv2.CAP_PVAPI, cv2.CAP_OPENNI, cv2.CAP_OPENNI_ASUS, cv2.CAP_ANDROID, cv2.CAP_XIAPI,
                  cv2.CAP_AVFOUNDATION, cv2.CAP_GIGANETIX, cv2.CAP_MSMF, cv2.CAP_WINRT, cv2.CAP_INTELPERC,
                  cv2.CAP_OPENNI2, cv2.CAP_OPENNI2_ASUS, cv2.CAP_GPHOTO2, cv2.CAP_GSTREAMER, cv2.CAP_FFMPEG,
                  cv2.CAP_IMAGES, cv2.CAP_ARAVIS, cv2.CAP_INTEL_MFX,
                  cv2.CAP_XINE]

  def _small_api(self):
    """
    Only apis that where somehow important
    during my testing and on my system.
    """
    return [cv2.CAP_DSHOW, cv2.CAP_MSMF]

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
            if(ret):
              if(self.create_temp_dir):
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
