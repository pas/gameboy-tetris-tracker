from abc import ABC, abstractmethod

import PySimpleGUI as sg

class Window(ABC):
  @abstractmethod
  def name(self):
    pass

  def finalize(self):
    return False

  def modal(self):
    return False

  def create(self):
    self.window = sg.Window(self.name(), self.layout(), modal=self.modal(), finalize=self.finalize())
    self._window_create_hook()
    self._event_loop()
    self.window.close()

  @abstractmethod
  def layout(self):
    pass

  def _event_loop(self):
    leave_event_loop = False
    while not leave_event_loop:
      event, values = self.window.read()
      if event in (sg.WIN_CLOSED, 'Exit'):
        self._window_close_hook()
        break
      leave_event_loop = self._event_loop_hook(event, values)

  def _window_close_hook(self):
    pass

  def _window_create_hook(self):
    pass

  @abstractmethod
  def _event_loop_hook(self, event, values):
    pass
