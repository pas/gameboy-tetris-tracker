from tetristracker.tracker.level_tracker import LevelTracker
from tetristracker.tracker.lines_tracker import LinesTracker
from tetristracker.tracker.score_tracker import ScoreTracker


class Stats():
  def __init__(self):
    self.singles = 0
    self.doubles = 0
    self.triples = 0
    self.tetris = 0
    self.scoring = [40, 100, 300, 1200]

  def get_tetris_rate(self):
    if (self.get_lines() == 0):
      return 1

    return self.get_tetris_lines() / self.get_lines()

  def get_lines(self):
    return self.singles + 2 * self.doubles + 3 * self.triples + self.get_tetris_lines()

  def get_tetris_lines(self):
    return 4 * self.tetris

  def _checkScoreWithLevel(self, score, level, lines):
    """
    https://tetris.wiki/Scoring
    40 x (level+1)
    100 x (level+1)
    300 x (level+1)
    1200 x (level+1)
    """
    return score == self.scoring[lines-1]*(level+1)

  def calculate(self, lines_tracker: LinesTracker,
                score_tracker: ScoreTracker,
                level_tracker: LevelTracker):

    level_change = False
    if (level_tracker.is_accepted()):
      if (level_tracker.difference() > 0):
        print("--- LEVEL CHANGE ---")
        level_change = True

    if (not lines_tracker.is_empty()
        and lines_tracker.is_accepted()
        and score_tracker.is_accepted()
        and level_tracker.is_accepted()
        and lines_tracker.accepted != 0):

      line_diff: int = lines_tracker.difference()
      if line_diff is not None and line_diff != 0:
        # This is shortly after lines cleared animation
        # The lines update after the lines cleared
        # animation.
        score_diff = score_tracker.difference()
        level = level_tracker.last()
        if level_change:
          level -= 1
        print("Level: " + str(level))

        if (line_diff > 4):
          print("Upps...")
          print("points: " + str(score_diff))
        else:
          check = self._checkScoreWithLevel(score_diff, level, line_diff)
          if (line_diff == 4):
            print("Tetris: " + str(score_diff) + "(" + str(check) + ")")
            self.tetris += 1
          if (line_diff == 3):
            self.triples += 1
            print("Triple: " + str(score_diff) + "(" + str(check) + ")")
          if (line_diff == 2):
            self.doubles += 1
            print("Double: " + str(score_diff) + "(" + str(check) + ")")
          if (line_diff == 1):
            self.singles += 1
            print("Single: " + str(score_diff) + "(" + str(check) + ")")

        if (self.get_lines() != lines_tracker.accepted):
          print("lines: " + str(self.get_lines()))
          print("line tracker: " + str(lines_tracker.accepted))

    if (not lines_tracker.is_empty()
        and lines_tracker.is_accepted()
        and score_tracker.is_accepted()):
      # We catch cases here where the points are already updated
      # but the line count not. Those we simply reject and
      # hope that we'll be able to track this in the next image

      line_diff: int = lines_tracker.difference()

      if line_diff is not None and line_diff == 0:
        # This is short after piece lock as
        # push down points are immediately added
        # to the score but we don't always have
        # push down points
        score_diff = score_tracker.difference()
        print("Push Down Points: " + str(score_diff))
        # TODO: This should not be here but it felt like it was the best place
        # TODO: because of the checks that happend before
        # This cannot be correct as you can make no more than 20 pushdown points
        if (score_diff > 20):
          print("Reject score value in after thought...")
          score_tracker.reject()

