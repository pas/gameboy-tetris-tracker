import matplotlib
from matplotlib import pyplot as plt
import numpy as np

class PieceDistributionPlotter:
  # L, J, I, O, Z, S, T
  # from https://babeheim.com/blog/2020-12-29-is-tetris-biased/
  expected_percentage = [0.107, 0.136, 0.137, 0.161, 0.138, 0.160, 0.161]

  def __init__(self, file_name="piece-distribution", mode="Original"):
    # Don't want to use the GUI
    matplotlib.use('Agg')
    self.file_name = file_name
    self.mode = mode

  def show_plot(self, _unused2, _unused1, piece_occurrences, show_expected=False):
    """
    Expects pieces in order

    """
    fig, ax = plt.subplots()

    summed_n = sum(piece_occurrences)
    txt = "n = " + str(summed_n)
    fig.text(.5, 0, txt, ha='center')

    b = np.array(piece_occurrences)
    ind = np.array([1, 4, 3, 0, 6, 5, 2])
    rearranged_piece_occurrences = np.empty(b.shape)
    rearranged_piece_occurrences[ind] = b

    names = ['L', 'J', 'I', 'O', 'Z', 'S', 'T']
    bar_colors = ['tab:grey', 'tab:grey', 'tab:grey', 'tab:grey']

    ax.bar(names, rearranged_piece_occurrences, color=bar_colors)

    if(show_expected):
      res = PieceDistributionPlotter.expected_percentage * np.array(summed_n)
      res = res.round()

      left_pad = 0.032
      # draw targets
      for index, height in enumerate(res):
        distance = 0.935/len(res)
        start = distance*(index+0.5)
        pad = 0.05
        ax.axhline(y=height, color='red', linestyle='--', linewidth=1, xmin=start - pad + left_pad, xmax=start + pad + left_pad)

    ax.set_ylabel('Occurrences')
    ax.set_title('Gameboy Tetris Piece Distribution: ' + self.mode)

    # This sometimes fails probably if
    # OBS opens the file at exactly the
    # same time as it tries to write.
    try:
      fig.savefig("plots/"+self.file_name+".png")
    except:
      print("Could not create plot")

    plt.close(fig)