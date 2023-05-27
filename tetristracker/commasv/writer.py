from abc import abstractmethod


class Writer:
  headers = ["time", "score", "lines", "level", "preview", "playfield"]

  @abstractmethod
  def write(self, score, lines, level, preview, playfield):
    pass