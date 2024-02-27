from tetristracker.capturer.mss_capturer import MSSCapturer
from tetristracker.capturer.interceptor_capturer import InterceptorCapturer
from tetristracker.capturer.obs_virtual_cam_capturer import OBSVirtualCamCapturer
from tetristracker.helpers.config import Config

class CaptureSelection:
  def __init__(self, config : Config):
    print(config)
    self.capturer = None
    self.name = ""
    self.config = config

  def get(self):
    return self.capturer

  def select(self, name):
    print(name)
    if(name == "interceptor"):
      self.select_interceptor()
    if(name == "screen"):
      self.select_screen()
    if(name == "obs"):
      self.select_obs_virtual_cam()

  def select_interceptor(self):
    self.name = "interceptor"
    self.capturer = InterceptorCapturer(self.config, create_temp_dir=False)

  def select_screen(self):
    self.name = "screenshot"
    bounding_box = self.config.get_screen_bounding_box()
    self.capturer = MSSCapturer(bounding_box, images_per_second=30)

  def select_obs_virtual_cam(self):
    self.name = "obs"
    bounding_box = self.config.get_obs_bounding_box()
    self.capturer = OBSVirtualCamCapturer(bounding_box, self.config, create_temp_dir=False)