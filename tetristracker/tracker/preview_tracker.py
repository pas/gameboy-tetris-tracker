from tetristracker.image.stats_image import StatsImage
from tetristracker.tracker.playfield_tracker import PlayfieldTracker
from tetristracker.tracker.tracker import Tracker


class PreviewTracker(Tracker):
  def __init__(self):
    super().__init__()
    self.stats = [0, 0, 0, 0, 0, 0, 0]
    self.stats_image = StatsImage()

  def track(self, preview, playfield_tracker : PlayfieldTracker):
    self._update_stats(preview, playfield_tracker)
    super().track(preview)

  def _update_stats(self, preview, playfield_tracker : PlayfieldTracker):
    clean_playfield = playfield_tracker.clean_playfield()
    print(clean_playfield)
    if(clean_playfield):
      if (self.last_clean_playfield and clean_playfield):
        print(self.last_clean_playfield.mino_difference(clean_playfield))
      self.last_clean_playfield = clean_playfield

    if(preview != self.last()):
      self.stats[preview] += 1
      self.stats_image.create_image(self.stats)
