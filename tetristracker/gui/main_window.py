import PySimpleGUI as sg

from tetristracker import retrieve_bounding_box
from tetristracker.capturer.capture_selection import CaptureSelection
from tetristracker.gui.camera_selection_popup import SelectCameraPopupWindow
from tetristracker.gui.stoppable_thread import StoppableThread
from tetristracker.gui.window import Window
from tetristracker.helpers.config import Config
from tetristracker.runner import Runner


class MainWindow(Window):
  MENU_ICEPT = 0
  MENU_SCREEN = 1
  MENU_OBS = 2

  capture_menu_default = [ 'interceptor::_ICEPT_',
                             'screen::_SCREEN_',
                             'obs virtual cam::_OBS_']

  def __init__(self, image_creator_window, scores, replay):
    # This is needed here because MSS sets this option as well
    # Otherwise the GUI will change as soon mss gets called.
    # See: https://github.com/PySimpleGUI/PySimpleGUI/issues/6392#event-9357175964
    sg.set_options(dpi_awareness=True)
    self.image_creator_window = image_creator_window
    self.scores_window = scores
    self.replay_window = replay
    self.window = None
    self.capture_selection = CaptureSelection()

  def layout(self):
    self.menu_def = [['Others', ['Retrieve bounding box::_BBOX_',
                            'Image creator::_CREATOR_',
                            "Highscores::_SCORES_",
                            "View replay::_REPLAY_",
                            "Camera selection::_CAMERA-SELECTION_"]],
                ['Capture', MainWindow.capture_menu_default]
                ]

    return [
      [sg.Menu(self.menu_def, key='_MENU_')],
      [sg.Button("Start", key="_START_", size=(40, 8))],
      [sg.Button("Stop", key="_STOP_", size=(40, 8))],
    ]

  def name(self):
    return "Main window"

  def _event_loop_hook(self, event, values):
    print(event)
    config = Config()
    if (event == "_START_"):
      self.thread = StoppableThread(target=start_capturing, args=(self.window,), daemon=True)
      self.thread.start()
    if (event == "_STOP_"):
      if(self.thread):
        self.thread.stop()
    if ("::" in event):
      split = event.split("::")[-1]
      if(split == "_BBOX_"):
        retrieve_bounding_box.run()
      if(split == "_CREATOR_"):
        self.image_creator_window.create()
      if(split == "_SCORES_"):
        self.scores_window.create()
      if(split == "_REPLAY_"):
        self.replay_window.create()
      if(split == "_CAMERA-SELECTION_"):
        self.create_camera_selection()
      if(split == "_ICEPT_"):
        config.set_capturer("interceptor")
        self.update_menu(MainWindow.MENU_ICEPT)
      if(split == "_SCREEN_"):
        config.set_capturer("screen")
        self.update_menu(MainWindow.MENU_SCREEN)
      if(split == "_OBS_"):
        config.set_capturer("obs")
        self.update_menu(MainWindow.MENU_OBS)


  def update_menu(self, index):
    self.menu_def[1][1] = MainWindow.capture_menu_default.copy()
    self.menu_def[1][1][index] = "(x) " + self.menu_def[1][1][index]
    self.window["_MENU_"].update(self.menu_def)

  def create_camera_selection(self):
    camera_selection_window = SelectCameraPopupWindow(self, use_case=self.capture_selection.name)
    camera_selection_window.create()


def start_capturing(window):
  # create capturer (this seems to have to be inside
  # the local thread or else mss doesn't work)
  builder = CaptureSelection()
  config = Config()
  builder.build(config.get_capturer())

  runner = Runner(capturer=builder.capturer)
  runner.run()
