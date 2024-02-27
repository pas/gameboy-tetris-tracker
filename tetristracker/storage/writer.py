from abc import abstractmethod


class Writer:
  headers = ["time", "score", "lines", "level", "preview", "playfield"]

  @abstractmethod
  def write(self, score : int, lines : int, level : int, preview : int, tetromino_in_play : int, spawned : bool, playfield):
    """
    :param score: current score
    :param lines: current number of lines
    :param level: current level
    :param preview: visible tetromino in preview
    :param tetromino_in_play: tetromino in play
    :param spawned: True if the tetromino just spawned. False otherwise.
    :param playfield: current playfield as numpy array 10x18 as ints
    """
    pass

  @abstractmethod
  def restart(self):
    """
    Resets the id
    """
    pass