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
        break
      leave_event_loop = self._event_loop_hook(event, values)

  @abstractmethod
  def _event_loop_hook(self, event, values):
    pass
