import numpy as np
import cv2

import tetristracker.unit.playfield as pf
from tetristracker.tile.tile_recognizer import TileRecognizer
from tetristracker.tile.tiler import Tiler
from tetristracker.tile.tile import Tile


class PlayfieldProcessor():
  """
  Processes the (tiled) playfield image
  into an array.
  Detects if the playfield image is in an
  ambigous state (e.g. it holds a
  blurred image)
  """
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

        # If we detect a non-white tile where
        # the minimum color (black) is above a
        # certain threshold (the blackest pixel is not full black)
        # then it is probably a tile that results from blurring between
        # two states and therefor the playfield is in transition
        if(not tile.is_white()):
          if(tile.get_min() > PlayfieldProcessor.THRESHHOLD):
            in_transition = True
            if(return_on_transition):
              return None

        # If we detect a one-colored non-white, non-black tile then
        # it's the line clear animation. We return such tiles
        # as grey.We should probably move this into the tile recognizer
        if(not tile.is_black() and not tile.is_white() and (tile.is_one_color() or tile.is_dull())):
          result.append(TileRecognizer.GREY)
        else:
          result.append(self.recognizer.recognize(tile_image))

    playfield = pf.Playfield(np.array(result).reshape(18, 10), in_transition=in_transition)
    playfield.full_row_replacement()

    return playfield

  def tile_image(self):
    tiler = Tiler(self.needed_number_of_tiles_height, self.needed_number_of_tiles_width, self.original_image)
    return tiler.adapted_image