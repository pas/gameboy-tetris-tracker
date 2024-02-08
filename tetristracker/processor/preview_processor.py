import cv2
import numpy as np

from tetristracker.tile.tile_recognizer import TileRecognizer
from tetristracker.tile.tiler import Tiler


class AreaProcessor():
  """
  This processor recognizes if one kind of mino (and
  only one kind) can be found in a specified area.
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
    self.ambiguous = True

  def tile_image(self):
    tiler = Tiler(self.nr_of_tiles_height, self.nr_of_tiles_width, self.original_image)
    return tiler.adapted_image

  def run(self, save_tiles=False):
    """
    Sets the ambigous flag if the preview
    consists not of exactly two tiles. A white
    tile and a mino.
    The ambigous flag is therefor set probably
    either if the game is on pause (then the
    preview is completly white) or on a
    transition (then more than one mino
    gets recognized).
    """
    result = []
    for column_nr, column in enumerate(self.tiled_image):
      for row_nr, tile in enumerate(column):
        if(save_tiles):
          cv2.imwrite('screenshots/tiles/' + str(column_nr) + "-" + str(row_nr) + '-screenshot-preview-tile.png', tile)
        result.append(self.recognizer.recognize(tile, simplify_i_mino=True))

    unique, counts = np.unique(result, return_counts=True)

    # Ambiguous if not
    # 1) Exactly two different tiles detected: mino and white
    # 2) Exactly twelve white tiles (therefor 4 minos)
    self.ambiguous = not unique.shape[0] == 2 and not counts[0] == 12

    # This only works because white is the smaller value
    # than minos.
    return result[np.argmax(result)]

class PreviewProcessor(AreaProcessor):
  def __init__(self, image, image_is_tiled=False):
    super().__init__(image, 4, 4, image_is_tiled)

class SpawningProcessor(AreaProcessor):
  def __init__(self, image, image_is_tiled=False):
    super().__init__(image, 2, 4, image_is_tiled)