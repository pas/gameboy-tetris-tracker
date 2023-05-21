from matplotlib import pyplot as plt

from tetristracker.helpers import calculations
from tetristracker.commasv.csv_reader import CSVReader


class Plotter:
  def calculate_points(self, number_of_lines, level):
    multiplier = [40, 100, 300, 1200]
    mult = multiplier[number_of_lines-1]
    return mult*(level+1)

  def get_worst_score_table(self):
    worst_score = []
    worst_lines = range(1,301)

    last_score = 0
    for line in range(1,301):
      if(line < 100):
        level = 9
      elif(line < 200):
        level = int(line/10)
      else:
        level = 20

      last_score = self.calculate_points(1, level) + last_score
      worst_score.append(last_score)

    return worst_score, worst_lines

  def get_perfect_score_table(self):
    perfect_score = []
    perfect_lines = []
    last_score = 0
    for _ in range(1,26):
      last_score = self.calculate_points(4, 9) + last_score
      perfect_score.append(last_score)

      if(len(perfect_lines) > 0):
        perfect_lines.append(perfect_lines[-1] + 4)
      else:
        perfect_lines.append(4)

    last_score = self.calculate_points(3,10) + last_score
    perfect_score.append(last_score)
    perfect_lines.append(perfect_lines[-1] + 3)

    for level in range(1,6):
      for _ in range(1,3):
        last_score = self.calculate_points(4, (level*2-1)+9) + last_score
        perfect_score.append(last_score)
        perfect_lines.append(perfect_lines[-1] + 4)
      for _ in range(1,4):
        last_score = self.calculate_points(4, level*2+9) + last_score
        perfect_score.append(last_score)
        perfect_lines.append(perfect_lines[-1] + 4)

    for _ in range(1,26):
      last_score = self.calculate_points(4, 20) + last_score
      perfect_score.append(last_score)
      perfect_lines.append(perfect_lines[-1] + 4)

    return perfect_score, perfect_lines

  def add_slope(self, slope, ax):
    x_min, x_max = ax.get_xlim()
    y_min, y_max = 0, slope * (x_max - x_min)
    ax.plot([x_min, x_max], [y_min, y_max])
    ax.set_xlim([x_min, x_max])

  def get_limits(self, current_max_score, current_max_lines):
    score = 100000

    if current_max_score > 100000:
      score = 500000
    if current_max_score > 500000:
      score = 999999

    lines = 100
    if current_max_lines > 100:
      lines = 200
    if current_max_lines > 200:
      lines = 300

    return score, lines

  def add_lower_bound(self, ax):
    scores, lines = self.get_worst_score_table()
    ax.scatter(lines, scores, s=1, c='r')

  def add_upper_bound(self, ax):
    scores, lines = self.get_perfect_score_table()
    ax.scatter(lines, scores, s=1, c='g')

  def add_current_best(self, ax):
    reader = CSVReader("best", "test/csv/")
    reader.set_delimiter(",")
    lines, scores = reader.get_lines_and_scores()
    ax.scatter(lines, scores, s=1, c='y')

  def show_plot(self, scores, lines):
    if(len(scores) > 3):
      fig, ax = plt.subplots()
      ax.scatter(lines, scores, c='b')
      self.add_lower_bound(ax)
      self.add_upper_bound(ax)
      self.add_current_best(ax)

      top, right = self.get_limits(scores[len(scores)-1], lines[len(lines)-1])
      ax.set_xlim(left=0, right=right)
      ax.set_ylim(bottom=0, top=top)
      if(len(lines) > 0 and max(scores) != min(scores) and max(lines) != min(lines)):
        slope = calculations.get_slope(lines, scores)
        self.add_slope(slope, ax)

      # This sometimes fails probably if
      # OBS opens the file at exactly the
      # same time as it tries to write.
      try:
        fig.savefig(r'plots/test.png')
      except:
        print("Could not create plot")

      plt.close(fig)