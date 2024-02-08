from tetristracker.gui.high_score_window import HighscoreWindow
from tetristracker.gui.image_creator_window import ImageCreatorWindow
from tetristracker.gui.main_window import MainWindow
from tetristracker.gui.replay_window import ReplayWindow
from tetristracker.helpers.config import Config

if __name__ == "__main__":
  image_creator = ImageCreatorWindow()
  scores = HighscoreWindow()
  replay = ReplayWindow()
  main = MainWindow(image_creator, scores, replay)
  config = Config()
  main.create()
  main.set_menu()  # doesn't work, yet because it does not get called as main.create() starts the main loop :(
