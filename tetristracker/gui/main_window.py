import PySimpleGUI as sg

from tetristracker import retrieve_bounding_box
from tetristracker.gui.stoppable_thread import StoppableThread
from tetristracker.gui.window import Window
from tetristracker.runner import Runner


class MainWindow(Window):
  def __init__(self, image_creator_window, scores, replay):
    # This is needed here because MSS sets this option as well
    # Otherwise the GUI will change as soon mss gets called.
    # See: https://github.com/PySimpleGUI/PySimpleGUI/issues/6392#event-9357175964
    sg.set_options(dpi_awareness=True)
    self.image_creator_window = image_creator_window
    self.scores_window = scores
    self.replay_window = replay
    self.window = None

  def layout(self):
    menu_def = [['Others', ['Retrieve bounding box::_BBOX_',
                            'Image creator::_CREATOR_',
                            "Highscores::_SCORES_",
                            "View replay::_REPLAY_"]]]

    return [
      [sg.Menu(menu_def, key='_MENU_')],
      [sg.Button("Start", key="_START_", size=(40, 8))],
      [sg.Button("Stop", key="_STOP_", size=(40, 8))],

    ]

  def name(self):
    return "Main window"

  def _event_loop_hook(self, event, values):
    print(event)
    if (event == "_START_"):
      self.thread = StoppableThread(target=start_capturing, args=(self.window,), daemon=True)
      self.thread.start()
    if (event == "_STOP_"):
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


def start_capturing(window):
  runner = Runner()
  runner.run()
