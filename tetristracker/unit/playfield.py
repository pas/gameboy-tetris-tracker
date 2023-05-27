from typing_extensions import Self

import numpy as np

from tetristracker.image.playfield_recreator import PlayfieldRecreator
# done because it resolves the problem with circular dependencies https://stackoverflow.com/questions/5748946/pythonic-way-to-resolve-circular-import-statements
import tetristracker.processor.playfield_processor as pp
from tetristracker.tile.tetromino import Tetromino
from tetristracker.tile.tetromino_transmission import TetrominoTransmission
from tetristracker.tile.tile_recognizer import TileRecognizer


class Playfield():
  # Using a method here so if the index for an empty
  # field should change that this still works
  @staticmethod
  def empty():
    return Playfield(np.full((pp.PlayfieldProcessor.needed_number_of_tiles_height, pp.PlayfieldProcessor.needed_number_of_tiles_width),
                   TileRecognizer.EMPTY))

  @staticmethod
  def checkerboard_mask(start=1):
    """
    Either start=1 or start=0. Everything
    else creates non-sensical data.
    """
    x = np.zeros((pp.PlayfieldProcessor.needed_number_of_tiles_height, pp.PlayfieldProcessor.needed_number_of_tiles_width), dtype=bool)
    x[0::2, 1::2] = 1
    x[1::2, 0::2] = 1

    if(start==0):
      x = np.roll(x, 1, axis=1)

    return x

  def __init__(self, playfield_as_array, in_transition=False):
    self.playfield_array = playfield_as_array
    self.line_clear_count = 0
    self.in_transition = in_transition

  def full_row_replacement(self):
    # binarize array
    array = self.all_but(TileRecognizer.GREY).binarize()
    # then sum each row
    summed_rows = np.sum(array, axis=1)
    # get indices with full row (10)
    self.line_clear_count = (summed_rows == 10).sum()
    self.playfield_array[summed_rows == 10] = -99

  def is_line_clear(self):
    return self.line_clear_count > 0

  def simplify_i_piece(self):
    array = self.playfield_array.copy()
    # This is not cool. This should be constants somewhere...
    array[(array >= 6) & (array <= 11)] = 6
    return Playfield(array)

  def only_one_type_of_mino(self):
    """
    Returns True if the playfield has only
    one type of mino.
    Returns False it the playfield is white
    or holds multiple types of minos.
    This simplifies the i to the same
    minos so each of them is counted
    as the same mino (which is normally
    not the case as each part of
    the i-piece has its own number)
    """
    playfield = self.simplify_i_piece()
    unique = np.unique(playfield.playfield_array)
    mino_type = TileRecognizer.EMPTY
    if(unique.shape[0] == 2):
      mino_type = unique[1]
    return unique.shape[0] == 2, mino_type

  def surface_trace(self):
    binarized = self.binarize()
    # fill gaps with any number
    rotated = np.rot90(binarized).cumsum(axis=-1)
    # replace numbers back to ones
    rotated[rotated > 0] = 1
    # sum together to get height
    rotated = np.cumsum(rotated, axis=-1)
    # rotated and subtract n1-n2, n2-n3, etc.
    trace = np.flip(np.max(rotated, axis=-1))
    diff = np.diff(trace)
    return diff

  def possibilities(self):
    trace = self.surface_trace()
    possibilities = []
    l1_surface = Tetromino.get_surface_array_l1()
    possibilities.append(TetrominoTransmission.I_TETROMINO)
    l2_surface = Tetromino.get_surface_array_l2()
    select_l2 = None
    for value in trace:
      if(value <= 2 and value >= -2):
        possibilities += l1_surface[value]
        if(select_l2):
          possibilities += select_l2[value]
        select_l2 = l2_surface[value]
      else:
        # Throw away previous selection if noting can fit
        select_l2 = None
    return np.unique(np.array(possibilities))

  def parity(self):
    mask1 = Playfield.checkerboard_mask()
    mask2 = Playfield.checkerboard_mask(start=0)
    binarized = self.binarize()
    return np.abs(np.sum(binarized[mask1])-np.sum(binarized[mask2]))

  def has_empty_line_at(self, line_number):
    """
    Line number has to be between 0 and 17
    """
    number_of_empty_spaces = (self.playfield_array[line_number] == TileRecognizer.EMPTY).sum()
    return number_of_empty_spaces == pp.PlayfieldProcessor.needed_number_of_tiles_width

  def count_minos(self, without_cleared_lines=False):
    """
    This takes into account previously cleared lines.
    Use without_cleared_lines if this is not
    what you want.
    """
    array = self.binarize()
    nr_of_minos_in_cleared_lines = 0
    if(not without_cleared_lines):
      nr_of_minos_in_cleared_lines =  self.line_clear_count * pp.PlayfieldProcessor.needed_number_of_tiles_width
    return np.sum(array) + nr_of_minos_in_cleared_lines

  def all_but(self, mino_index):
    """
    Use fixed values from TileRecognizer
    as index, for example TileRecognizer.J_MINO
    """
    reduced = self.playfield_array.copy()
    reduced[reduced != mino_index] = TileRecognizer.EMPTY
    return Playfield(reduced)

  def mino_difference(self, previous_playfield):
    """
    This does subtract the mino size from
    the previous playfield from this playfield
    therefore playfield1.mino_difference(playfield2)
    is equal -1*playfield2.mino_difference(playfield1)
    """
    return previous_playfield.count_minos()-self.count_minos()

  def same_minos(self, other_playfield : Self):
    """
    Returns True if there are the same minos
    on both playfield withouth considering
    their position
    """
    uniques, counts = np.unique(self.playfield_array, return_counts=True)
    uniques2, counts2 = np.unique(other_playfield.playfield_array, return_counts=True)
    return np.array_equal(uniques, uniques2) and np.array_equal(counts, counts2)

  def intersection(self, playfield):
    intersection = self.playfield_array.copy()
    intersection[self.binarize() & playfield.binarize() == 0] = TileRecognizer.EMPTY
    return intersection

  def difference(self, playfield : Self):
    """
    Returns a play field with all overlapping
    elements removed. This does not care if
    the overlapping elements are the same
    mino or not.
    """
    difference = self.playfield_array.copy()
    difference[self.binarize() & playfield.binarize() == 1] = TileRecognizer.EMPTY
    return Playfield(difference)

  def is_equal(self, previous_playfield : Self):
    """
    This does not take into account the cleared
    line. Calculates an exact playfield difference
    and it is zero then this is true
    """
    summed_difference = (self.playfield_array - previous_playfield.playfield_array).sum()
    return summed_difference == 0

  def playfield_difference(self, previous_playfield: Self):
    """
    Returns a playfield that only shows the
    minos on tiles that are not already taken
    by the previous playfield. Be aware that
    that it does not care if the minos at the tiles that
    are ignored are the same or not.
    Example:
    p1 = [[1,2,-99][-99,-99,-99]]
    p2 = [[-99,1,-99][-99,-99,2][
    p1.playfield_difference(p2)
    -> [[1,-99,-99][-99,-99,-99]]
    p2.playfield_difference(p1)
    -> [[-99,-99,-99],[-99,-99,2]]
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
