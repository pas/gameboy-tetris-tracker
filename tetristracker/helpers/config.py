import yaml


class Config():
  def __init__(self, path="config.yml"):
    self.path = path
    self.config = None

  def _load(self):
    with open(self.path, 'r') as config_file:
      self.config= yaml.safe_load(config_file)

  def _dump(self):
    with open(self.path, 'w') as file:
      yaml.dump(self.config, file)

  def get_bounding_box(self):
    self._load()
    return self.config["bounding_box"]

  def set_bounding_box(self, bounding_box):
    self._load()
    self.config["bounding_box"] = bounding_box
    self._dump()

  def get_capturer(self):
    self._load()
    return self.config["capturer"]

  def set_capturer(self, capturer):
    self._load()
    self.config["capturer"] = capturer
    self._dump()





