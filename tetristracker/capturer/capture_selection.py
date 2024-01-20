import yaml

from tetristracker.capturer.mss_capturer import MSSCapturer
from tetristracker.capturer.interceptor_capturer import InterceptorCapturer
from tetristracker.capturer.obs_virtual_cam_capturer import OBSVirtualCamCapturer


class CaptureSelection:
  def __init__(self):
    self.capturer = None
    self.name = ""

  def build(self, name):
    if(name == "interceptor"):
      self.select_interceptor()
    if(name == "screen"):
      self.select_screen()
    if(name == "obs"):
      self.select_obs_virtual_cam()

  def select_interceptor(self):
    self.name = "interceptor"
    self.capturer = InterceptorCapturer(create_temp_dir=False)

  def select_screen(self, config="config.yml"):
    self.name = "screenshot"
    with open(config, 'r') as config_file:
      self.configs = yaml.safe_load(config_file)
      bounding_box = self.configs["bounding_box"]
      self.capturer = MSSCapturer(bounding_box)

  def select_obs_virtual_cam(self, config="config.yml"):
    self.name = "obs_virtual_cam"
    with open(config, 'r') as config_file:
      self.configs = yaml.safe_load(config_file)
      bounding_box = self.configs["obs_virtual_cam_capturer"]["bounding_box"]
      self.capturer = OBSVirtualCamCapturer(bounding_box, create_temp_dir=False)