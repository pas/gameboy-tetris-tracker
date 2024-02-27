import numpy as np

from tetristracker.image.stats_image import StatsImage
from tetristracker.tile.tile_recognizer import TileRecognizer
from tetristracker.tracker.playfield_tracker import PlayfieldTracker
from tetristracker.tracker.tracker import Tracker
from tetristracker.unit.playfield import Playfield


class PreviewTracker(Tracker):
  def __init__(self):
    super().__init__()
    self.stats = [0, 0, 0, 0, 0, 0, 0]
    self.stats_image = StatsImage()
    # This is the preview before
    # the spawning of the current
    # piece => it's the piece
    # in play
    self.remember_preview = None
    self.last_clean_playfield = None
    self.spawned_piece = None
    self.tetromino_spawned = False

  def track(self, preview, playfield_tracker : PlayfieldTracker):
    # What happens if there is no last value, e.g. if somebody starts
    # at a pause?

    # If somebody passes a value that is either -1 or None
    # we assume that the last preview was the correct one
    if preview == -1 or preview is None:
      preview = self.last()

    self._update(preview, playfield_tracker)
    super().track(preview)

  def reset_spawning(self):
    self.tetromino_spawned = False

  def force_count(self, mino):
    """
    This will count the given mino
    as a tetromino that has spawned
    """
    self.tetromino_spawned = True
    self.remember_preview = mino
    self._update_stats(None)

  def _update_stats(self, current_preview):
    # This should be the case if the same pieces
    # spawns again. We detected a change in the
    # number of tetrominos but no change in the preview
    if self.remember_preview == TileRecognizer.EMPTY:
      self.remember_preview = current_preview
    self.spawned_piece = self.remember_preview
    self.stats[self.remember_preview] += 1
    self.stats_image.create_image(self.stats)
    # We reset and therefor marking it as consumed
    self.remember_preview = TileRecognizer.EMPTY

  def _update(self, current_preview, playfield_tracker : PlayfieldTracker):
    if self.remember_preview is None:
      self.remember_preview = current_preview

    # Reset flag indicating that a tetromino just spawned
    self.tetromino_spawned = False

    clean_playfield = playfield_tracker.clean_playfield()
    if isinstance(clean_playfield, np.ndarray):
      clean_playfield = Playfield(clean_playfield)
      if self.last_clean_playfield:
        # This is the case if there was no line clear
        if self.last_clean_playfield.mino_difference(clean_playfield) == 4:
          difference = clean_playfield.difference(self.last_clean_playfield)
          self.tetromino_spawned, _ = difference.only_one_type_of_mino()
        # This is the case if there was a line clear
        if self.last_clean_playfield.mino_difference(clean_playfield) < -1:
          self.tetromino_spawned = True
      self.last_clean_playfield = clean_playfield

    # This is need because we need two images to detect a change correctly
    # This get triggered if the piece in the preview changes
    # then it gets consumed in the next round
    if not (self.last() is None) and current_preview != self.last():
      self.remember_preview = self.last()


    # There are two different situation that need to be considered:
    # 1) The preview shows a different tetromino
    # 2) The preview shows the same tetromino (because the same piece got selected again)
    # This should be triggered only once after a new piece got spawned
    if self.tetromino_spawned:
      self._update_stats(current_preview)
