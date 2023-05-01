import numpy as np
import cv2
from tile_recognizer import TileRecognizer, Tiler
from playfield_recreator import PlayfieldRecreator

class Playfield():
  def __init__(self, playfield_as_array):
    self.playfield_array = playfield_as_array

  def full_row_replacement(self):
    # binarize array
    array = self.binarize()
    # then sum each row
    summed_rows = np.sum(array, axis=1)
    # get indices with full row (10)
    self.playfield_array[summed_rows == 10] = -99

  def count_minos(self):
    array = self.binarize()
    return np.sum(array)

  def all_but(self, mino_index):
    """
    Use fixed values from TileRecognizer
    as index, for example TileRecognizer.J_MINO
    """
    reduced = self.playfield_array.copy()
    reduced[reduced != mino_index] = -99
    return Playfield(reduced)

  def mino_difference(self, previous_playfield):
    """
    This does return subtracts the mino size from
    the previous playfield from this playfield
    therefore playfield1.mino_difference(playfield2)
    is not the same as playfield2.mino_difference(playfield1)
    """
    return previous_playfield.count_minos()-self.count_minos()

  def playfield_difference(self, previous_playfield):
    """
    Returns a playfield that only shows the
    minos on tiles that are not already taken
    by the previous playfield. Be aware that
    it ignores if the minos at the tiles that
    are ignored are the same or not.
    """
    binarized_previous = previous_playfield.binarize()
    binarized_difference = binarized_previous - self.binarize()
    mask = binarized_difference == 0
    masked_playfield = self.playfield_array.copy()
    masked_playfield[mask] = -99
    return Playfield(masked_playfield)

  def binarize(self):
    """
    Does create a binary array. Where 1 is
    any mino and 0 is white
    """
    array = self.playfield_array.copy()
    array[array > -99] = 1
    array[array == -99] = 0
    return array

  def recreate(self, path):
    recreator = PlayfieldRecreator()
    recreator.recreate(self.playfield_array, path)

class PlayfieldProcessor():
  needed_number_of_tiles_width = 10
  needed_number_of_tiles_height = 18
  names = ["J-mino", "Z-mino", "O-mino", "L-mino", "T-mino", "S-mino",
           "I-top-vertical-mino", "I-center-vertical-mino", "I-bottom-vertical-mino",
            "I-left-horizontal-mino", "I-center-horizontal-mino", "I-right-horizontal-mino",
           "border left", "border bottom", "border right", "border top"]

  # Probably better just pass the dimensions here and then pass the image in run phase
  # because it changes. Otherwise we always have to recreate everything...
  def __init__(self, image, image_is_tiled=False):
    """
    Expects either array, ScreenShot object from mss or numpy array.
    """
    self.original_image = self.adapted_image = np.array(image)
    if(image_is_tiled):
      self.tiled_image = np.array(image)
    else:
      self.tiled_image = self.tile_image()
    self.recognizer = TileRecognizer()

  def run(self, save_tiles=False):
    result = []

    for column_nr, column in enumerate(self.tiled_image):
      for row_nr, tile in enumerate(column):
        if(save_tiles):
          cv2.imwrite('test/tiles/' + str(column_nr) + "-" + str(row_nr) + '-screenshot-tile.png', tile)
        result.append(self.recognizer.recognize(tile))

    playfield = Playfield(np.array(result).reshape(18, 10))
    playfield.full_row_replacement()

    return playfield

  def tile_image(self):
    tiler = Tiler(self.needed_number_of_tiles_height, self.needed_number_of_tiles_width, self.original_image)
    return tiler.adapted_image