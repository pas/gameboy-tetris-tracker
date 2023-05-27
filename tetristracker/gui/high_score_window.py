from tetristracker.commasv.sqlite_reader import SqliteReader
from tetristracker.commasv.sqlite_writer import SqliteWriter
from tetristracker.gui.window import Window

import PySimpleGUI as sg

class HighscoreWindow(Window):
  def __init__(self):
    _ = SqliteWriter() # we initialize it here, so we can make sure that the database and the tables exists
    reader = SqliteReader()
    values = reader.get_start_and_end_times_per_round()
    text = ""
    for value in values:
      text += str(value) + "\n"
    self.output = sg.Multiline(text, key="_OUTPUT_", size=(200,20))


  def layout(self):
    return [[self.output]]

  def name(self):
    return "Scores"

  def finalize(self):
    return True

  def modal(self):
    return True

  def _event_loop_hook(self, event, values):
    return False








