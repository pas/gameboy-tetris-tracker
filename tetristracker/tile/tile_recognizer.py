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

  def __init__(self,):
    if(len(TileRecognizer.mino_array) == 0):
      self.create_mino_array()

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

      template_matching_values = self.matching(tile.tile_image)
      best_match = np.argmax(template_matching_values)

      if(simplify_i_mino and best_match > TileRecognizer.I_MINO_SIMPLE):
        best_match = TileRecognizer.I_MINO_SIMPLE

      # Seems to be difficult for template matching
      # to correctly identify the L piece. Checking
      # for brightness and only decide between
      # L-Mino and S-Mino should help
      # We are looking for white in center
      if (tile.brightness() < 95):
        # The center of the S-Mino is bright
        if(tile.center_brightness() > 100):
          best_match = TileRecognizer.S_MINO
        else:
          best_match = TileRecognizer.L_MINO


    return best_match

  def matching(self, tile):
    methods = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR',
               'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']

    result = []
    for mino_template in TileRecognizer.mino_array:
      match_value = cv2.matchTemplate(tile, mino_template, eval(methods[0]))
      result.append(match_value)

    return np.array(result).flatten()

  def retrieve_template(self, path):
    image = Image.open(path).convert('L').resize((Tile.STANDARD_WIDTH, Tile.STANDARD_HEIGHT), Image.Resampling.BILINEAR)
    return np.array(image)

  def create_mino_array(self):
    j_mino = self.retrieve_template("images/tiles/81.png") #0
    z_mino = self.retrieve_template("images/tiles/82.png") #1
    o_mino = self.retrieve_template("images/tiles/83.png") #2
    l_mino = self.retrieve_template("images/tiles/84.png") #3
    t_mino = self.retrieve_template("images/tiles/85.png") #4
    s_mino = self.retrieve_template("images/tiles/86.png") #5

    t1_mino = self.retrieve_template("images/tiles/80.png") #6
    t2_mino = self.retrieve_template("images/tiles/88.png")
    t3_mino = self.retrieve_template("images/tiles/89.png")
    t1r_mino = self.retrieve_template("images/tiles/8A.png")
    t2r_mino = self.retrieve_template("images/tiles/8B.png")
    t3r_mino = self.retrieve_template("images/tiles/8F.png")

    #This needs to be in the same order as the names
    TileRecognizer.mino_array =  [
            j_mino,                 z_mino,               o_mino,                 l_mino,                   t_mino,
            s_mino,                 t1_mino,              t2_mino,                t3_mino,                  t1r_mino,
            t2r_mino,               t3r_mino,]
            #edge_case_border_left,  edge_case_border_bottom,  edge_case_border_right, edge_case_border_top]