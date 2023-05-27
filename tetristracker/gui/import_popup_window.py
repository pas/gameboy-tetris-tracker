import csv
from pathlib import Path
import PySimpleGUI as sg

from tetristracker.gui.window import Window


class ImportPopupWindow(Window):
  def __init__(self, master_window):
    self.master_window = master_window

  def name(self):
    return "Open file"

  def finalize(self):
    return True

  def modal(self):
    return True

  def layout(self):
    return [
      [
        sg.Input(key='-INPUT-'),
        sg.FileBrowse(file_types=(("TXT Files", "*.txt"), ("ALL Files", "*.*"))),
        sg.Button("Import", key="_IMPORT_"),
      ]
    ]

  def _event_loop_hook(self, event, values):
    leave_event_loop = False

    if event == "_IMPORT_":
      filename = values['-INPUT-']
      if Path(filename).is_file():
        try:
          with open(filename, "rt", encoding='utf-8') as csv_file:
            reader = csv.reader(csv_file, delimiter=";")
            for row_nr, row in enumerate(reader):
              for column_nr, tile_nr in enumerate(row):
                path = self.master_window.get_path(int(tile_nr))
                button = self.master_window.image_layout[row_nr][column_nr]
                button.key().data = int(tile_nr)
                button.update(image_filename=path)
            leave_event_loop = True

        except Exception as e:
          print(e)
          print("Could not open file! Your image should only consist of numbers")

    return leave_event_loop
