import numpy as np
import cv2
from tile_recognizer import TileRecognizer, Tiler, Tile
from playfield_recreator import PlayfieldRecreator

class Playfield():
  # Using a method here so if the index for an empty
  # field should change that this still works
  @staticmethod
  def empty():
    return Playfield(np.full((PlayfieldProcessor.needed_number_of_tiles_height, PlayfieldProcessor.needed_number_of_tiles_width),
                   TileRecognizer.EMPTY))

  def __init__(self, playfield_as_array, in_transition=False):
    self.playfield_array = playfield_as_array
    self.line_clear_count = 0
    self.in_transition = in_transition

  def full_row_replacement(self):
    # binarize array
    array =self.all_but(TileRecognizer.GREY).binarize()
    #array = self.binarize()
    # then sum each row
    summed_rows = np.sum(array, axis=1)
    # get indices with full row (10)
    self.line_clear_count = (summed_rows == 10).sum()
    self.playfield_array[summed_rows == 10] = -99

  def is_line_clear(self):
    return self.line_clear_count > 0

  def has_empty_line_at(self, line_number):
    """
    Line number has to be between 0 and 17
    """
    number_of_empty_spaces = (self.playfield_array[line_number] == TileRecognizer.EMPTY).sum()
    return number_of_empty_spaces == PlayfieldProcessor.needed_number_of_tiles_width

  def count_minos(self, without_cleared_lines=False):
    """
    This takes into account previously cleared lines.
    Use without_cleared_lines if this is not
    what you want.
    """
    array = self.binarize()
    nr_of_minos_in_cleared_lines = 0
    if(not without_cleared_lines):
      nr_of_minos_in_cleared_lines =  self.line_clear_count * PlayfieldProcessor.needed_number_of_tiles_width
    return np.sum(array) + nr_of_minos_in_cleared_lines

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

  def is_equal(self, previous_playfield):
    """
    This does not take into account the cleared
    line. Calculates an exact playfield differenc
    and it is zero then this is true
    """
    summed_difference = (self.playfield_array - previous_playfield.playfield_array).sum()
    return summed_difference == 0

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
  THRESHHOLD = 300
  needed_number_of_tiles_width = 10
  needed_number_of_tiles_height = 18
  names = ["J-mino", "Z-mino", "O-mino", "L-mino", "T-mino", "S-mino",
           "I-top-vertical-mino", "I-center-vertical-mino", "I-bottom-vertical-mino",
            "I-left-horizontal-mino", "I-center-horizontal-mino", "I-right-horizontal-mino",
           "border left", "border bottom", "border right", "border top"]

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

  def run(self, save_tiles=False, return_on_transition=False):
    """
    When return on transition then it
    immediately returns if the playfield
    is on transition. The return value
    is None
    """
    result = []

    in_transition = False

    for column_nr, column in enumerate(self.tiled_image):
      for row_nr, tile_image in enumerate(column):
        tile = Tile(tile_image, row_nr=row_nr, column_nr=column_nr)

        if (save_tiles):
          cv2.imwrite('screenshots/tiles/' + str(column_nr) + "-" + str(row_nr) + '-screenshot-tile.png', tile.tile_image)

        if(not tile.is_white()):
          if(tile.get_min() > PlayfieldProcessor.THRESHHOLD):
            in_transition = True
            if(return_on_transition):
              return None

        # If we detect a one-colored non-white tile then
        # it's the tetris animation. We should probably
        # move this into the tile recognizer
        if(not tile.is_black() and not tile.is_white() and (tile.is_one_color() or tile.is_dull())):
          result.append(TileRecognizer.GREY)
        else:
          result.append(self.recognizer.recognize(tile_image))

    playfield = Playfield(np.array(result).reshape(18, 10), in_transition=in_transition)
    playfield.full_row_replacement()

    return playfield

  def tile_image(self):
    tiler = Tiler(self.needed_number_of_tiles_height, self.needed_number_of_tiles_width, self.original_image)
    return tiler.adapted_image