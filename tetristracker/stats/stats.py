from tetristracker.tracker.level_tracker import LevelTracker
from tetristracker.tracker.lines_tracker import LinesTracker
from tetristracker.tracker.score_tracker import ScoreTracker


class Stats():
  def __init__(self):
    self.singles = 0
    self.doubles = 0
    self.triples = 0
    self.tetris = 0

  def get_tetris_rate(self):
    if(self.get_lines() == 0):
      return 1

    return self.get_tetris_lines() / self.get_lines()

  def get_lines(self):
    return self.singles + 2*self.doubles + 3*self.triples + self.get_tetris_lines()

  def get_tetris_lines(self):
    return 4*self.tetris

  def calculate(self, lines_tracker : LinesTracker,
                      score_tracker : ScoreTracker,
                      level_tracker : LevelTracker):

    if( not lines_tracker.is_empty()
        and lines_tracker.is_accepted()
        and score_tracker.is_accepted()
        and level_tracker.is_accepted()
        and lines_tracker.accepted != 0 ):

      line_diff : int = lines_tracker.difference()
      if line_diff is not None and line_diff != 0:
        score_diff = score_tracker.difference()
        level = level_tracker.last()

        if(line_diff > 4):
          print("Upps...")

        if(line_diff == 4):
          self.tetris += 1
        if(line_diff == 3):
          self.triples += 1
        if(line_diff == 2):
          self.doubles += 1
        if(line_diff == 1):
          self.singles += 1

        assert(self.get_lines() == lines_tracker.accepted)
