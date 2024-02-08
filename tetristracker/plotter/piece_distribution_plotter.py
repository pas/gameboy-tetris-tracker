import matplotlib
from matplotlib import pyplot as plt
import numpy as np

class PieceDistributionPlotter:
  def __init__(self, file_name="piece-distribution"):
    # Don't want to use the GUI
    matplotlib.use('Agg')
    self.file_name = file_name

  def show_plot(self, _unused2, _unused1, piece_occurrences):
    """
    Expects pieces in order:

    """
    fig, ax = plt.subplots()

    txt = "n = " + str(sum(piece_occurrences))
    fig.text(.5, 0, txt, ha='center')

    b = np.array(piece_occurrences)
    ind = np.array([1, 4, 3, 0, 6, 5, 2])
    rearranged_piece_occurrences = np.empty(b.shape)
    rearranged_piece_occurrences[ind] = b

    names = ['L', 'J', 'I', 'O', 'Z', 'S', 'T']
    bar_colors = ['tab:grey', 'tab:grey', 'tab:grey', 'tab:grey']

    ax.bar(names, rearranged_piece_occurrences, color=bar_colors)

    ax.set_ylabel('Occurrences')
    ax.set_title('Gameboy Tetris Piece Distribution')

    # This sometimes fails probably if
    # OBS opens the file at exactly the
    # same time as it tries to write.
    try:
      fig.savefig("plots/"+self.file_name+".png")
    except:
      print("Could not create plot")

    plt.close(fig)