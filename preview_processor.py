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

  def tile_image(self):
    tiler = Tiler(PreviewProcessor.nr_of_tiles_height, PreviewProcessor.nr_of_tiles_width, self.original_image)
    return tiler.adapted_image

  def run(self, save_tiles=False):
    result = []
    for column_nr, column in enumerate(self.tiled_image):
      for row_nr, tile in enumerate(column):
        if(save_tiles):
          cv2.imwrite('test/tiles/' + str(column_nr) + "-" + str(row_nr) + '-screenshot-preview-tile.png', tile)
        result.append(self.recognizer.recognize(tile, simplify_i_mino=True))

    unique = np.unique(result)

    if(unique.shape[0] > 2):
      print(result)

    assert(unique.shape[0] == 2)
    assert(unique[0] == -99)

    return result[np.argmax(result)]