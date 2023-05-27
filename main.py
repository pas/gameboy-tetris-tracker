from tetristracker.gui.high_score_window import HighscoreWindow
from tetristracker.gui.image_creator_window import ImageCreatorWindow
from tetristracker.gui.main_window import MainWindow


if __name__ == "__main__":
  image_creator = ImageCreatorWindow()
  scores = HighscoreWindow()
  main = MainWindow(image_creator, scores)
  main.create()
