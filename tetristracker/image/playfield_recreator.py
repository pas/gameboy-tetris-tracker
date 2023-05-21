import cv2
import numpy as np
from PIL import Image


class PlayfieldRecreator():
  def __init__(self):
    self.tiles = self._load_tiles()

  def recreate(self, playfield_array, path):
    for column_nr, column in enumerate(playfield_array):
      for row_nr, tile_nr in enumerate(column):
        if(tile_nr == -99):
          tile_nr = 12
        tile = self.tiles[tile_nr]
        if(row_nr > 0):
          row = np.concatenate((row,tile), axis=1)
        else:
          row = tile
      if(column_nr > 0):
        result = np.concatenate((result, row), axis=0)
      else:
        result = row

    cv2.imwrite(path, result)

    return result

  def _open_image(self, path):
    return np.array(Image.open(path).convert('RGB'))

  def _load_tiles(self):
    return [
      self._open_image("images/tiles/81.png"), #j
      self._open_image("images/tiles/82.png"), #z
      self._open_image("images/tiles/83.png"), #o
      self._open_image("images/tiles/84.png"), #l
      self._open_image("images/tiles/85.png"), #t
      self._open_image("images/tiles/86.png"), #s

      self._open_image("images/tiles/80.png"), #t1
      self._open_image("images/tiles/88.png"), #t2
      self._open_image("images/tiles/89.png"), #t3
      self._open_image("images/tiles/8A.png"), #t4
      self._open_image("images/tiles/8B.png"), #i5
      self._open_image("images/tiles/8F.png"), #i6

      self._open_image("images/tiles/2F.png"), #white
    ]