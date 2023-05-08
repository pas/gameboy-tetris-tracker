import cv2
import numpy as np

from tile_recognizer import TileRecognizer, Tiler


class PreviewProcessor():
  nr_of_tiles_height = 4
  nr_of_tiles_width = 4

  def __init__(self, image, image_is_tiled=False):
    self.original_image = np.array(image)
    if(image_is_tiled):
      self.tiled_image = np.array(image)
    else:
      self.tiled_image = self.tile_image()

    self.recognizer = TileRecognizer()
    self.ambigous = True

  def tile_image(self):
    tiler = Tiler(PreviewProcessor.nr_of_tiles_height, PreviewProcessor.nr_of_tiles_width, self.original_image)
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