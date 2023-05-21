from tetristracker.processor.playfield_processor import Playfield
from tetristracker.tracker.simple_tracker import SimpleTracker


class PlayfieldTracker(SimpleTracker):
  def __init__(self):
    super().__init__()
    self.current : Playfield = None
    self.previous : Playfield = None
    self.clean : Playfield = None
    self.only_tetromino : Playfield = None

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
      # if the difference is 8 the same piece is still in play

      # if the difference is 4 the the previous image was
      # cought at the exact time the previous piece locked
      # and a new piece just spawned
      if (difference.count_minos()==4):
        self.clean = self.current.intersection(self.previous)
      return self.clean
    else:
      return None

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
