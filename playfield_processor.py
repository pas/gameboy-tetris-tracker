import numpy as np
import cv2
from tile_recognizer import TileRecognizer, Tiler


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

    return np.array(result).reshape(18, 10)

  def tile_image(self):
    tiler = Tiler(self.needed_number_of_tiles_height, self.needed_number_of_tiles_width, self.original_image)
    return tiler.adapted_image