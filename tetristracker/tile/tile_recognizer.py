import numpy as np
from PIL import Image
import cv2

from tetristracker.tile.tile import Tile


class TileRecognizer:
  J_MINO = 0
  Z_MINO = 1
  O_MINO = 2
  L_MINO = 3
  T_MINO = 4
  S_MINO = 5
  I_MINO_SIMPLE = 6
  GREY = 12
  EMPTY = -99
  mino_array = []
  finished_tile = None

  def __init__(self,):
    if(len(TileRecognizer.mino_array) == 0):
      self.create_mino_array()
      TileRecognizer.finished_tile = self.retrieve_template("images/tiles/87.png")

  def is_finished_tile(self, tile : []):
    """
    We brake here with the pattern that we
    make checks in the Tile object. We add a
    check for this here because this not necessary
    for all 180 tiles but only for the one
    in the left bottom corner
    TODO: We could do this differently by just call another method for this tile...
    """
    best_match = -99 # default is a white tile
    tile = Tile(tile)

    # Skip white tiles
    if not tile.is_white():
      # If we detect a one-colored non-white, non-black tile then
      # it's the line clear animation. We return such tiles
      # as grey.We should probably move this into the tile recognizer
      if not tile.is_black() and (tile.is_one_color() or tile.is_dull()):
        return False

      appended_mino_array = TileRecognizer.mino_array.copy()
      appended_mino_array.append(TileRecognizer.finished_tile)
      result = []

      for i, mino_template in enumerate(appended_mino_array):
        diff = np.abs(tile.tile_image.astype('int') - mino_template.astype('int'))
        match_value = np.sum(diff)
        result.append(match_value)

      result = np.array(result).flatten()
      best_match = np.argmin(result)

    return best_match == 12

  def recognize(self, tile, simplify_i_mino=False):
    """
    :param tile:
    :param simplify_t_mino: Replaces all found T-minos
    with the value of T_MINO_SIMPLE
    :return:
    """
    best_match = -99 # default is a white tile
    tile = Tile(tile)

    # Skip white tiles
    if not tile.is_white():
      # If we detect a one-colored non-white, non-black tile then
      # it's the line clear animation. We return such tiles
      # as grey.We should probably move this into the tile recognizer
      if not tile.is_black() and (tile.is_one_color() or tile.is_dull()):
        return TileRecognizer.GREY

      template_matching_values = self.simplistic_matching(tile.tile_image)
      best_match = np.argmin(template_matching_values)

      if(simplify_i_mino and best_match > TileRecognizer.I_MINO_SIMPLE):
        best_match = TileRecognizer.I_MINO_SIMPLE

    return best_match

  def matching(self, tile : []):
    methods = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR',
               'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']

    result = []
    for mino_template in TileRecognizer.mino_array:
      match_value = cv2.matchTemplate(tile, mino_template, eval(methods[0]))
      result.append(match_value)

    return np.array(result).flatten()

  def simplistic_matching(self, tile : np.ndarray):
    result = []

    for i, mino_template in enumerate(TileRecognizer.mino_array):
      diff = np.abs(tile.astype('int') - mino_template.astype('int'))
      match_value = np.sum(diff)
      result.append(match_value)

    return np.array(result).flatten()


  def retrieve_template(self, path):
    image = Image.open(path).convert('L').resize((Tile.STANDARD_WIDTH, Tile.STANDARD_HEIGHT), Image.Resampling.BOX)
    return np.array(image)

  def create_mino_array(self):
    j_mino = self.retrieve_template("images/tiles/81.png") #0
    z_mino = self.retrieve_template("images/tiles/82.png") #1
    o_mino = self.retrieve_template("images/tiles/83.png") #2
    l_mino = self.retrieve_template("images/tiles/84.png") #3
    t_mino = self.retrieve_template("images/tiles/85.png") #4
    s_mino = self.retrieve_template("images/tiles/86.png") #5

    t1_mino = self.retrieve_template("images/tiles/80.png") #6
    t2_mino = self.retrieve_template("images/tiles/88.png") #7
    t3_mino = self.retrieve_template("images/tiles/89.png") #8
    t1r_mino = self.retrieve_template("images/tiles/8A.png") #9
    t2r_mino = self.retrieve_template("images/tiles/8B.png") #10
    t3r_mino = self.retrieve_template("images/tiles/8F.png") #11

    #This needs to be in the same order as the names
    TileRecognizer.mino_array =  [
            j_mino,                 z_mino,               o_mino,                 l_mino,                   t_mino,
            s_mino,                 t1_mino,              t2_mino,                t3_mino,                  t1r_mino,
            t2r_mino,               t3r_mino,]
            #edge_case_border_left,  edge_case_border_bottom,  edge_case_border_right, edge_case_border_top]