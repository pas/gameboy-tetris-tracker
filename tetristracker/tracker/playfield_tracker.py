from tetristracker.tracker.simple_tracker import SimpleTracker
from tetristracker.unit.playfield import Playfield


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
    piece on it.

    Returns the last clean playfield if no new clean
    playfield was found.

    Returns None if not two at least tow playfields exists
    or if no clean playfield could be found.
    """
    if(self.previous):
      difference = self.previous.difference(self.current).count_minos()
      # if difference is 0 minos then it is still the same image

      # if the difference is 2-3, 5-8 minos the same piece is still in play

      # if the difference is 4 minos the the previous image was
      # cought at the exact time the previous piece locked
      # and a new piece just spawned
      # TODO: There is an exception: If the image capture is unfortunate
      # then it might be that the piece in play has an overlap of exactly
      # two pieces. This would lead to the 4 minos difference
      if (difference==4 and not self.previous.same_minos(self.current)):
        # We check again. If it is clean we should not have
        # empty lines below any mino on the playfield
        might_clean = self.current.intersection(self.previous)

        # some error checking as sometimes the same_minos does not
        # kick in the case of wrong tile recognition
        # TODO: This does not work in all cases...
        if not Playfield(might_clean).has_gaps():
          self.clean = might_clean

      return self.clean
    else:
      return None

  def was_line_clear(self):
    """
    Returns true if the previous image had a
    line clear.
    Calculates the difference between the
    number of minos. If this is negative
    (< -2) then there was a line clear.

    TODO: Currently only used in tests...
    """
    line_clear_detected = False
    if(self.previous):
      mino_difference = self.previous.mino_difference(self.current)
      line_clear_detected = mino_difference < -2
    return line_clear_detected

  def only_active_tetromino(self):
    """
    Returns the playfield with only the active
    tetromino. Everything else is white.

    TODO: Currently only used in tests...
    """
    if self.previous:
      difference = self.previous.difference(self.current)
      if difference.count_minos() == 4:
        self.only_tetromino = difference
        return self.only_tetromino
    elif self.current.count_minos() == 4:
      # This captures the case at the beginning
      # where there is no previous playfield
      # TODO: This should not be necessory anymore as we start always with an empty playfield
      self.only_tetromino = self.current
      return self.only_tetromino
    else:
      return None
