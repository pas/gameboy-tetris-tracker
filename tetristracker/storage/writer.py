from abc import abstractmethod


class Writer:
  headers = ["time", "score", "lines", "level", "preview", "playfield"]

  @abstractmethod
  def write(self, score, lines, level, preview, playfield):
    pass

  @abstractmethod
  def restart(self):
    """
    Resets the id
    """
    pass