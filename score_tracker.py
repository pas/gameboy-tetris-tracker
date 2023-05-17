from playfield_processor import Playfield
from stats_image import StatsImage


class SimpleTracker:
  def __init__(self):
    self.current = -1
    self.previous = -1

  def track(self, value):
    self.previous = self.current
    self.current = value

class PlayfieldTracker(SimpleTracker):
  def __init__(self):
    super().__init__()
    self.current = None
    self.previous = None
    self.clean = None
    self.only_tetromino = None

  def track(self, playfield):
    super().track(playfield)

  def clean_playfield(self):
    """
    Returns a playfield that has no falling
    piece on it. Returns None if not
    two playfields exists or no clean
    playfield could be found. If this does
    not suceed it simply returns the last
    clean playfield
    """
    if(self.previous):
      difference = self.previous.difference(self.current)
      if (difference.count_minos()==4):
        self.clean = self.current.intersection(self.previous)
      return self.clean
    else:
      return None

  def tetromino_distance(self):
    """
    Calculates distance of current active
    tetromino to the last available position
    of a tetromino.
    If the last available tetromino was not
    the same tetromino then this returns
    None
    """
    last = self.only_tetromino
    current = self.only_active_tetromino()
    print(current)

    if(current is None or last is None):
      return None

    print(last.tetromino_distance(current))

  def only_active_tetromino(self):
    """
    Returns the playfield with only the active
    tetromino. Everything else is white.
    """
    if(self.previous):
      difference = self.previous.difference(self.current)
      if(difference.count_minos()==4):
        self.only_tetromino = difference
        return self.only_tetromino
    elif(self.current.count_minos() == 4):
      self.only_tetromino = self.current
      return self.only_tetromino
    else:
      return None



class Tracker:
  """
  Only tracks ints
  """
  def __init__(self):
    self.accepted = -1
    self.array = []

  def track(self, value):
    """
    A None value gets tracked as -1
    but does not update the
    accepted_score value
    """
    if (value != None):
      self.accepted = value
      self.array.append(int(value))
    else:
      self.array.append(-1)

  def is_accepted(self):
    return not self.array[len(self.array) - 1] == -1

  def is_empty(self):
    return len(self.array) == 0

  def last(self):
    """
    Returns always None if there is no value stored
    """
    if(len(self.array) > 0):
      return self.array[len(self.array) - 1]
    else:
      return None

  def has_changed(self):
    """
    Returns always false if there is only one value stored.
    """
    if(len(self.array) > 1):
      return self.array[len(self.array)-1] != self.array[len(self.array)-2]
    else:
      return False

class LargerOrEqualTracker(Tracker):
  def track(self, value):
    """
    The check for >= is a little bit of false value prevention (not a good one though...)
    """
    if(value != None):
      if(value < self.accepted):
        value = -1
    else:
      value = -1

    super().track(value)

class ScoreTracker(LargerOrEqualTracker):
  # This is just to make the code clear
  def track(self, score):
    super().track(score)

class LinesTracker(LargerOrEqualTracker):
  # This is just to make the code clear
  def track(self, lines):
    super().track(lines)

class LevelTracker(LargerOrEqualTracker):
  # This is just to make the code clear
  def track(self, level):
    super().track(level)

class PreviewTracker(Tracker):
  def __init__(self):
    super().__init__()
    self.stats = [0, 0, 0, 0, 0, 0, 0]
    self.stats_image = StatsImage()

  def track(self, preview, force_update=False):
    super().track(preview)
    self._update_stats(preview, force_update)

  def _update_stats(self, preview, force_update):
    if(preview != self.last() or force_update):
      self.stats[preview] += 1
      self.stats_image.create_image(self.stats)

