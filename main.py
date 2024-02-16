from tetristracker.gui.high_score_window import HighscoreWindow
from tetristracker.gui.image_creator_window import ImageCreatorWindow
from tetristracker.gui.main_window import MainWindow
from tetristracker.gui.replay_window import ReplayWindow
from tetristracker.gui.trimmed_image_window import TrimmedImageWindow
from tetristracker.helpers.config import Config

if __name__ == "__main__":
  image_creator = ImageCreatorWindow()
  scores = HighscoreWindow()
  replay = ReplayWindow()
  trimmed_image_window = TrimmedImageWindow()
  main = MainWindow(image_creator, scores, replay, trimmed_image_window)
  config = Config()
  main.create()
  main.set_menu()  # doesn't work, yet because it does not get called as main.create() starts the main loop :(
