import cv2
import numpy as np

from tetristracker.tile.tile_recognizer import TileRecognizer
from tetristracker.tile.tiler import Tiler


class AreaProcessor():
  """
  This processor recognizes if one piece (and
  only one piece) can be found in a specific area.
  """
  def __init__(self, image, tiles_height, tiles_width, image_is_tiled=False):
    self.original_image = np.array(image)

    self.nr_of_tiles_height = tiles_height
    self.nr_of_tiles_width = tiles_width

    if(image_is_tiled):
      self.tiled_image = np.array(image)
    else:
      self.tiled_image = self.tile_image()

    self.recognizer = TileRecognizer()
    self.ambigous = True

  def tile_image(self):
    tiler = Tiler(self.nr_of_tiles_height, self.nr_of_tiles_width, self.original_image)
    return tiler.adapted_image

  def run(self, save_tiles=False):
    """
    Sets the ambigous flag if there the preview
    consists not of exactly two tiles. A white
    tile and a mino.
    The ambigous flag is therefor set probably
    to either the game is on pause (then the
    preview is completly white) or a
    transition (then more than one mino
    gets recognized).
    """
    result = []
    for column_nr, column in enumerate(self.tiled_image):
      for row_nr, tile in enumerate(column):
        if(save_tiles):
          cv2.imwrite('screenshots/tiles/' + str(column_nr) + "-" + str(row_nr) + '-screenshot-preview-tile.png', tile)
        result.append(self.recognizer.recognize(tile, simplify_i_mino=True))

    unique = np.unique(result)

    # Another good check would be if there are not
    # exactly four minos
    if(not unique.shape[0] == 2 and unique[0] == -99):
      self.ambigous = True
    else:
      self.ambigous = False

    return result[np.argmax(result)]

class PreviewProcessor(AreaProcessor):
  def __init__(self, image, image_is_tiled=False):
    super().__init__(image, 4, 4, image_is_tiled)

class SpawningProcessor(AreaProcessor):
  def __init__(self, image, image_is_tiled=False):
    super().__init__(image, 2, 4, image_is_tiled)