import PySimpleGUI as sg

from tetristracker import retrieve_bounding_box
from tetristracker.capturer.capture_selection import CaptureSelection
from tetristracker.storage.sqlite_writer import SqliteWriter
from tetristracker.gui.camera_selection_popup import SelectCameraPopupWindow
from tetristracker.gui.stoppable_thread import StoppableThread
from tetristracker.gui.window import Window
from tetristracker.helpers.config import Config
from tetristracker.plotter.plotter_selection import PlotterSelection
from tetristracker.runner import Runner


class MainWindow(Window):
  MENU_ICEPT = 0
  MENU_SCREEN = 1
  MENU_OBS = 2

  MENU_SCORE = 0
  MENU_PIECE_DIST = 1

  TOP_MENU_CAPTURER = 1
  TOP_MENU_MODE = 2

  capture_menu_default = [ 'interceptor::_ICEPT_',
                             'screen::_SCREEN_',
                             'obs virtual cam::_OBS_' ]

  mode_menu_default = [ 'highscore::_SCORE_',
                         'piece distribution::_PIECE_DIST_' ]

  def __init__(self, image_creator_window, scores, replay, trimmed_image_window):
    # This is needed here because MSS sets this option as well
    # Otherwise the GUI will change as soon mss gets called.
    # See: https://github.com/PySimpleGUI/PySimpleGUI/issues/6392#event-9357175964
    sg.set_options(dpi_awareness=True)
    self.image_creator_window = image_creator_window
    self.scores_window = scores
    self.replay_window = replay
    self.trimmed_image_window = trimmed_image_window
    self.window = None
    self.config = Config()

  def layout(self):
    self.menu_def = [['Others', ['Retrieve bounding box::_BBOX_',
                                 'View trimmed image::_TRIMMED_',
                            'Image creator::_CREATOR_',
                            "Highscores::_SCORES_",
                            "View replay::_REPLAY_",
                            "Camera selection::_CAMERA-SELECTION_"]],
                ['Capture', MainWindow.capture_menu_default],
                ['Mode', MainWindow.mode_menu_default]
                ]

    return [
      [sg.Menu(self.menu_def, key='_MENU_')],
      [sg.Button("Start", key="_START_", size=(40, 8))],
      [sg.Button("Stop", key="_STOP_", size=(40, 8))],
    ]

  def name(self):
    return "Main window"

  def set_menu(self):
    if self.config.get_capturer() == "screen":
      self._event_loop_hook("_SCREEN_", None)
    if self.config.get_mode() == "score":
      self._event_loop_hook("_SCORE_", None)

  def _event_loop_hook(self, event, values):
    if (event == "_START_"):
      self.thread = StoppableThread(target=start_capturing, args=(self.window, self, ), daemon=True)
      self.thread.start()
    if (event == "_STOP_"):
      if(self.thread):
        self.thread.stop()
    if ("::" in event):
      split = event.split("::")[-1]
      if(split == "_BBOX_"):
        retrieve_bounding_box.run(self.config)
      if(split == "_CREATOR_"):
        self.image_creator_window.create()
      if(split == "_SCORES_"):
        self.scores_window.create()
      if(split == "_REPLAY_"):
        self.replay_window.create()
      if(split == "_TRIMMED_"):
        self.trimmed_image_window.create()
      if(split == "_CAMERA-SELECTION_"):
        self.create_camera_selection()
      if(split == "_ICEPT_"):
        self.config.set_capturer("interceptor")
        self.update_capturer_menu(MainWindow.MENU_ICEPT)
      if(split == "_SCREEN_"):
        self.config.set_capturer("screen")
        self.update_capturer_menu(MainWindow.MENU_SCREEN)
      if(split == "_OBS_"):
        self.config.set_capturer("obs")
        self.update_capturer_menu(MainWindow.MENU_OBS)
      if(split == "_PIECE_DIST_"):
        self.update_mode_menu(MainWindow.MENU_PIECE_DIST)
      if(split == "_SCORE_"):
        self.update_mode_menu(MainWindow.MENU_SCORE)

  def update_menu(self, default_menu, menu_index, selection_index):
    self.menu_def[menu_index][1] = default_menu
    self.menu_def[menu_index][1][selection_index] = "(x) " + self.menu_def[menu_index][1][selection_index]
    self.window["_MENU_"].update(self.menu_def)

  def update_mode_menu(self, index):
    self.update_menu(MainWindow.mode_menu_default.copy(),
                     MainWindow.TOP_MENU_MODE,
                     index)

  def update_capturer_menu(self, index):
    self.update_menu(MainWindow.capture_menu_default.copy(),
                     MainWindow.TOP_MENU_CAPTURER,
                     index)

  def create_camera_selection(self):
    camera_selection_window = SelectCameraPopupWindow(self, self.config, use_case=self.config.get_capturer())
    camera_selection_window.create()

def start_capturing(window, self):
  config = Config()

  # create capturer (this seems to have to be inside
  # the local thread or else mss doesn't work)
  capture_selection = CaptureSelection(config)
  capture_selection.select(config.get_capturer())

  plotter_selection = PlotterSelection(config)
  plotter_selection.select(config.get_plotter())

  writer = SqliteWriter()

  runner = Runner(capturer=capture_selection.get(), writer=writer, plotter=plotter_selection.get(), shift_score=config.get_rom_version()=="gamescom")
  runner.run()
