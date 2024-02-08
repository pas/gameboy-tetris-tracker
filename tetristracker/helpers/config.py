import yaml

class Config():
  def __init__(self, path="config.yml"):
    self.path = path
    self.config = None

  def _load(self):
    with open(self.path, 'r') as config_file:
      self.config = yaml.safe_load(config_file)

  def _dump(self):
    with open(self.path, 'w') as file:
      yaml.dump(self.config, file)

  def get_screen_bounding_box(self):
    self._load()
    return self.config["screen"]["bounding_box"]

  def set_screen_bounding_box(self, bounding_box):
    self._load()
    self.config["screen"]["bounding_box"] = bounding_box
    self._dump()

  def _set_camera(self, index, api, name):
    self._load()
    self.config[name]["camera"]["index"] = index
    self.config[name]["camera"]["api"] = api
    self._dump()

  def set_interceptor_camera(self, index, api):
    self._set_camera(index, api, "interceptor")

  def set_obs_camera(self, index, api):
    self._set_camera(index, api, "obs")

  def _get_interceptor_camera_values(self, name):
    self._load()
    return self.config["interceptor"]["camera"][name]

  def get_interceptor_camera_index(self):
    return int(self._get_interceptor_camera_values("index"))

  def get_interceptor_camera_api(self):
    return self._get_interceptor_camera_values("api")

  def _get_obs_camera_values(self, name):
    self._load()
    return int(self.config["obs"]["camera"][name])

  def get_obs_camera_index(self):
    return self._get_obs_camera_values("index")

  def get_obs_camera_api(self):
    return self._get_obs_camera_values("api")

  def get_obs_bounding_box(self):
    self._load()
    return self.config["obs"]["bounding_box"]

  def set_obs_bounding_box(self, bounding_box):
    self._load()
    self.config["obs"]["bounding_box"] = bounding_box
    self._dump()

  def get_mode(self):
    self._load()
    return self.config["mode"]

  def get_rom_version(self):
    self._load()
    return self.config["rom_version"]

  def get_plotter(self):
    self._load()
    return self.config["plotter"]

  def set_mode(self, mode):
    self._load()
    self.config["mode"] = mode
    self._dump()

  def get_capturer(self):
    self._load()
    return self.config["capturer"]

  def set_capturer(self, capturer):
    self._load()
    self.config["capturer"] = capturer
    self._dump()





