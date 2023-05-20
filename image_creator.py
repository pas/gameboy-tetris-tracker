from abc import ABC, abstractmethod

import PySimpleGUI as sg
import cv2
import numpy as np
from PIL import Image


class Position:
  def __init__(self, row, column):
    self.row = row
    self.column = column

class ButtonCall:
  def __init__(self, key, data):
    self.data = data
    self.key = key

  def call(self):
    return self

class ImageVisitor(ABC):
  @abstractmethod
  def start(self, image_layout):
    pass

  @abstractmethod
  def end(self, image_layout):
    pass

  @abstractmethod
  def row_start(self, image_layout, rownr, row):
    pass

  @abstractmethod
  def row_end(self, image_layout, rownr, row):
    pass

  @abstractmethod
  def column(self, image_layout, rownr, row, columnnr, column):
    pass

class StringBuilder(ImageVisitor):
  def __init__(self):
    self.string = ""

  def start(self, image_layout):
    self.string += "["

  def row_start(self, image_layout, row_nr, row):
    if(row_nr != len(image_layout)):
      self.string += "["

  def column(self, image_layout, row_nr, row, column_nr, tile):
    if column_nr != 0 and column_nr != len(row):
      self.string += ","
    self.string += str(tile.key().data)

  def row_end(self, image_layout, row_nr, row):
    self.string += "]"
    if row_nr != len(row):
      self.string += ",\n"

  def end(self, image_layout):
    self.string += "]"

  def get_string(self):
    return self.string

class ImageBuilder(ImageVisitor):
  def __init__(self):
    self.image = None
    self.row = None
    self.tiles = self._tiles_array()

  def _tiles_array(self):
    return [self._open_image(self._get_path(i)) for i in range(256)]

  def _open_image(self, path):
    return np.array(Image.open(path).convert('RGB'))

  def _get_path(self, number):
    hex_number = f'{number:02x}'.upper()
    return "images/tiles/" + hex_number + ".png"

  def start(self, image_layout):
    pass

  def row_start(self, image_layout, row_nr, row):
    pass

  def column(self, image_layout, row_nr, row, column_nr, tile):
    tile_image = self.tiles[tile.key().data]
    if column_nr > 0:
      self.row = np.concatenate((self.row, tile_image), axis=1)
    else:
      self.row = tile_image

  def row_end(self, image_layout, row_nr, row):
    if row_nr > 0:
      self.image = np.concatenate((self.image, self.row), axis=0)
    else:
      self.image = self.row

  def end(self, image_layout):
    pass

  def get_image(self):
    return self.image

class ArrayBuilder(ImageVisitor):
  def __init__(self):
    self.array = []
    self.row = None

  def start(self, image_layout):
    pass

  def row_start(self, image_layout, row_nr, row):
    self.row = []
    self.array.append(self.row)

  def column(self, image_layout, row_nr, row, column_nr, tile):
    self.row.append(tile.key().data)

  def row_end(self, image_layout, row_nr, row):
    pass

  def end(self, image_layout):
    pass

  def get_array(self):
    return self.array

class ImageCreator:
  def __init__(self):
    self.run()

  def get_path(self, number):
    hex_number = f'{number:02x}'.upper()
    return "images/tiles/" + hex_number + ".png"

  def visit_image(self, visitor):
    """
    Visitor gets called in each part of
    the loop
    """
    visitor.start(self.image_layout)
    for row_nr, row in enumerate(self.image_layout):
      visitor.row_start(self.image_layout, row_nr, row)
      for column_nr, tile in enumerate(row):
        visitor.column(self.image_layout, row_nr, row, column_nr, tile)
      visitor.row_end(self.image_layout, row_nr, row)
    visitor.end(self.image_layout)

  def run(self):
    WHITE = 47
    white_tile = self.get_path(WHITE)
    select = WHITE
    select_path = white_tile
    previous = None

    MAX_ROWS = 28
    MAX_COL = 33

    self.image_layout = [[sg.Button(image_filename=white_tile, size=(4, 2), key=ButtonCall("_IMAGE_", WHITE).call, pad=(0, 0)) for col in range(MAX_COL)] for row in range(MAX_ROWS)]
    self.select_layout = [[sg.Button(image_filename=self.get_path(j+i*16), border_width=3, size=(4,2), key=ButtonCall("_SELECT_", j+i*16).call, pad=(0,0)) for j in range(16)] for i in range(16)]
    layout = [[[sg.Frame("Create your background", layout=self.image_layout),
              sg.Frame("Select tile", layout=self.select_layout)], sg.Button("Save", key="_SAVE_")]]

    window = sg.Window('Create your own Tetris background', layout)

    while True:
      event, values = window.read()
      if event in (sg.WIN_CLOSED, 'Exit'):
        break

      if(event == "_SAVE_"):
        visitor = StringBuilder()
        self.visit_image(visitor)
        print(visitor.get_string())
        visitor = ArrayBuilder()
        self.visit_image(visitor)
        print(visitor.get_array())
        visitor = ImageBuilder()
        self.visit_image(visitor)
        cv2.imwrite("background.png", visitor.get_image())
      elif callable(event):
        if event().key == "_SELECT_":
          if(previous):
            window[previous].update(button_color=(sg.theme_background_color(), sg.theme_background_color()))
          select_path = self.get_path(event().data)
          select = event().data
          window[event].update(button_color=(sg.theme_background_color(), "#ff0000"))
          previous = event
        elif event().key == "_IMAGE_":
          event().data = select
          window[event].update(image_filename=select_path)

    window.close()

if __name__ == "__main__":
  ImageCreator()