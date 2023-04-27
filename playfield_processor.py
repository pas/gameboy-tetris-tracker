import numpy as np
from PIL import Image, ImageOps, ImageStat
import cv2
from tile_recognizer import TileRecognizer, Tiler

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

class PreviewProcessor():
  nr_of_tiles_height = 4
  nr_of_tiles_width = 4

  def __init__(self, image):
    self.original_image = np.array(image)
    self.tiled_image = self.tile_image()
    self.recognicer = TileRecognizer()

  def tile_image(self):
    tiler = Tiler(PreviewProcessor.nr_of_tiles_height, PreviewProcessor.nr_of_tiles_width, self.original_image)
    return tiler.adapted_image

  def run(self, save_tiles=False):
    result = []
    for column_nr, column in enumerate(self.tiled_image):
      for row_nr, tile in enumerate(column):
        if(save_tiles):
          cv2.imwrite('test/tiles/' + str(column_nr) + "-" + str(row_nr) + '-screenshot-preview-tile.png', tile)
        result.append(self.recognicer.recognize(tile, simplify_i_mino=True))

    unique = np.unique(result)

    if(unique.shape[0] > 2):
      print(result)

    assert(unique.shape[0] == 2)
    assert(unique[0] == -99)

    return result[np.argmax(result)]

class PlayfieldProcessor():
  needed_number_of_tiles_width = 12
  needed_number_of_tiles_height = 18
  names = ["J-mino", "Z-mino", "O-mino", "L-mino", "T-mino", "S-mino",
           "I-top-vertical-mino", "I-center-vertical-mino", "I-bottom-vertical-mino",
            "I-left-horizontal-mino", "I-center-horizontal-mino", "I-right-horizontal-mino",
           "border left", "border bottom", "border right", "border top"]

  # Probably better just pass the dimensions here and then pass the image in run phase
  # because it changes. Otherwise we always have to recreate everything...
  def __init__(self, image):
    """
    Expects either array, ScreenShot object from mss or numpy array.
    """
    self.original_image = self.adapted_image = np.array(image)
    self.tiled_image = self.tile_image()
    self.recognicer = TileRecognizer()

  def run(self):
    result = []

    for column_nr, column in enumerate(self.tiled_image):
      for row_nr, tile in enumerate(column):
        cv2.imwrite('test/tiles/' + str(column_nr) + "-" + str(row_nr) + '-screenshot-tile.png', tile)
        # Skip borders
        if (not (row_nr == 0 or row_nr == 11)):
          result.append(self.recognicer.recognize(tile))

    return np.array(result).reshape(18, 10)

  def tile_image(self):
    tiler = Tiler(self.needed_number_of_tiles_height, self.needed_number_of_tiles_width, self.original_image)
    return tiler.adapted_image







