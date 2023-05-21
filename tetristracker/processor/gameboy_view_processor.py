import cv2
import numpy as np

from tetristracker.tile.tile_recognizer import Tiler, Tile
from tetristracker.image.image_manipulator import convert_4bitgrey_to_grey


class GameboyViewProcessor():
  nr_of_tiles_width = 20
  nr_of_tiles_height = 18

  def __init__(self, image, save_tiles=False):
    self.original_image = np.array(image)
    self.tiled_image = self._tile_image()
    self._run(save_tiles=save_tiles)

  def _tile_image(self):
    tiler = Tiler(GameboyViewProcessor.nr_of_tiles_height, GameboyViewProcessor.nr_of_tiles_width, self.original_image)
    return tiler.adapted_image

  def _run(self, save_tiles=False):
    if(save_tiles):
      for column_nr, column in enumerate(self.tiled_image):
        for row_nr, tile in enumerate(column):
          tile_image = Tile(tile).tile_image
          cv2.imwrite('screenshots/tiles/' + str(column_nr) + "-" + str(row_nr) + '-full-view-tile.png',
                      convert_4bitgrey_to_grey(tile_image))

  def get_top_left_tile(self):
    return Tile(np.squeeze(self.tiled_image[0:1, 0:1].copy()))

  def get_continue(self):
    return self.tiled_image[9:10, 3:11].copy()

  def get_spawning_area(self):
    return self.tiled_image[1:3, 5:9].copy()

  def get_playfield(self):
    return self.tiled_image[0:18,2:12].copy()

  def get_preview(self):
    return self.tiled_image[13:17, 15:19].copy()

  def get_score(self):
    return self.tiled_image[3:4, 13:19].copy()

  def get_lines(self):
    return self.tiled_image[10:11, 15:18].copy()

  def get_level(self):
    return self.tiled_image[7:8, 16:18].copy()