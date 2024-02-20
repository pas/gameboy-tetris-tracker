import json

import PySimpleGUI as sg

from tetristracker.storage.sqlite_reader import SqliteReader
from tetristracker.gui.button_call import ButtonCall
from tetristracker.gui.image_creator_window import Position
from tetristracker.gui.window import Window
from tetristracker.helpers.calculations import number_to_image_path, tile_number_to_image_number
from tetristracker.recreator.replay_creator import ReplayCreator


class ReplayWindow(Window):
  def __init__(self):
    self.WHITE = 47
    self.white_tile = number_to_image_path(self.WHITE)
    self.MAX_ROWS = 18
    self.MAX_COL = 10
    self.round = None
    self.index = None

  def name(self):
    return "Replay"

  def layout(self):
    self.image_layout = [
      [sg.Image(self.white_tile, size=(20, 20), key=ButtonCall("_IMAGE_", Position(col, row)).call, pad=(0, 0)) for col in
       range(self.MAX_COL)] for row in range(self.MAX_ROWS)]
    self.button_layout = [[sg.Button("Load game", key="_LOAD_"),
                           sg.Combo(self._get_round_ids(), readonly=True, enable_events=False, key="_LIST_"),
                           sg.Button("Next", key="_NEXT_"),
                           sg.Button("Previous", key="_PREV_"),
                           sg.Button("Create B-Type replay", key="_SAVE_REPLAY_")]]
    return [self.image_layout, self.button_layout]

  def _get_round_ids(self):
    reader = SqliteReader()
    return reader.get_round_ids()

  def _event_loop_hook(self, event, values):
    if(event == "_LOAD_"):
      self._load()
    if(event == "_NEXT_"):
      self._next()
    if(event == "_PREV_"):
      self._previous()
    if(event == "_SAVE_REPLAY_"):
      self._save_replay()

  def _save_replay(self):
    if(self.creator):
      with open("screenshots/replay.txt", "w") as file:
        file.write(json.dumps(self.creator.create()))

  def _next(self):
    if(self.round != None):
      if(self.index < len(self.round)-1):
        self._update(self.index+1)

  def _previous(self):
    if(self.round != None):
      if(self.index > 0):
        self._update((self.index-1))

  def _update(self, new_index):
    self.creator.set_start_index(new_index)
    self._update_image(new_index)

  def _update_image(self, index):
    self.index = index
    data = self.round[index]
    self.image_array = data[SqliteReader.PLAYFIELD]
    for col_nr, col in enumerate(self.image_array):
      for row_nr, tile_nr in enumerate(col):
        self.image_layout[col_nr][row_nr].update(source=number_to_image_path(tile_number_to_image_number(tile_nr)))

  def _load(self):
    selected = self.window["_LIST_"].get()[0]
    if(selected != ""):
      reader = SqliteReader()
      round = reader.get_round(str(selected))
      if(len(round) > 0):
        self.round = round
        self.creator = ReplayCreator(self.round, 0)
        self._update_image(0)

  def finalize(self):
    return True