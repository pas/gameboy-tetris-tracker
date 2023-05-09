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


  def _accept(self, playfield):
    mino_difference = self.current.mino_difference(playfield)
    # I need a test for all those situation

    # a mino zero difference is when the piece is dropping
    # a mino four difference is when a new piece spawns
    # a same playfield situation is it during a line burn
    if (mino_difference != 4 and not playfield.is_equal(self.current) and mino_difference != 0):
      print("Some weird shit happening here! Mino difference: " + str(mino_difference))
      print("Nr minos previous: " + str(self.current.count_minos()))
      print("Nr minos current: " + str(playfield.count_minos()))
      #cv2.imwrite("test/wrong-difference-full-view.png", processor.original_image)
      playfield.recreate("test/wrong-difference-current.png")
      self.current.recreate("test/wrong-difference-previous.png")
      print("Lines cleared: " + str(playfield.line_clear_count))
      print("Lines cleared (previous): " + str(self.current.line_clear_count))
      # if(current_playfield.line_clear_count > 0 or accepted_playfield.line_clear_count > 0):
      # exit()
      # We skip weird shit...
    else:
      print("accept")
      # When two playfields are the same and there is a playfield that has registered
      # a line burn then we want to keep the one that has registered the line burn
      # this does not guarantee that the accepted playfield always correctly
      # registers the line burn, but it does guarantee that once it has registered
      # it, it doesn't get lost anymore
      if (not self.current.is_equal(playfield) or self.current.line_clear_count > 0):
        self.current = playfield

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
  # This is just to make the code clear
  def track(self, preview):
    super().track(preview)
