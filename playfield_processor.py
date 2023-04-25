import numpy as np
from PIL import Image, ImageOps, ImageStat
import cv2
from tile_recognizer import TileRecognizer

class PlayfieldProcessor():
  needed_number_of_tiles_width = 12
  needed_number_of_tiles_height = 18
  names = ["J-mino", "Z-mino", "O-mino", "L-mino", "T-mino", "S-mino",
           "I-top-vertical-mino", "I-center-vertical-mino", "I-bottom-vertical-mino",
            "I-left-horizontal-mino", "I-center-horizontal-mino", "I-right-horizontal-mino",
           "border left", "border bottom", "border right", "border top"]

  # Probably better just pass the dimensions here and then pass the image in run phase
  # because it changes. Otherwise we always have to recreate everything...
  def __init__(self, image):
    """
    Expects either array, ScreenShot object from mss or numpy array.
    """
    self.original_image = self.adapted_image = np.array(image)
    self.tile_height, self.tile_width = self.get_dimensions()
    self.tiled_image = self.tile_image()
    self.recognicer = TileRecognizer()

  def tile_image(self):
    return self.adapted_image.reshape(self.needed_number_of_tiles_height, self.tile_height, self.needed_number_of_tiles_width, self.tile_width, 4).swapaxes(1,2)

  def show_stats(self, image):
    shape = image.shape
    height = shape[0]
    width = shape[1]

    # Check if playfield can be divided evenly.
    even_height = height % self.needed_number_of_tiles_height
    even_width = width % self.needed_number_of_tiles_height
    print("Even height: " + str(even_height))
    print("Even width: " + str(even_width))

    # The playfield consists of 18x10 tiles
    number_of_tiles_height = height / self.needed_number_of_tiles_height
    number_of_tiles_width = width / self.needed_number_of_tiles_width
    print("Tile height: " + str(number_of_tiles_height))
    print("Tile width: " + str(number_of_tiles_width))

  def run(self):
    result = []

    for column_nr, column in enumerate(self.tiled_image):
      for row_nr, tile in enumerate(column):
        cv2.imwrite('test/tiles/' + str(column_nr) + "-" + str(row_nr) + '-screenshot-tile.png', tile)
        # Skip borders
        if (not (row_nr == 0 or row_nr == 11)):
          result.append(self.recognicer.recognize(tile))

    return np.array(result).reshape(18, 10)

  def get_dimensions(self):
    """
    Expects np.array (height,width,4)
    So the image is expected to be in RGBA!

    Stores tile_width and tile_height
    """
    shape = self.adapted_image.shape
    height = shape[0]
    width = shape[1]

    even_height = height % self.needed_number_of_tiles_height
    even_width = width % self.needed_number_of_tiles_width

    new_height = height + self.needed_number_of_tiles_height - even_height
    new_width = width + self.needed_number_of_tiles_width - even_width

    if(even_width > 0 or even_height > 0):
      self.adapted_image =  np.array(Image.fromarray(self.adapted_image).resize((new_width, new_height), Image.Resampling.BILINEAR))

    self.show_stats(self.adapted_image)

    height = self.adapted_image.shape[0]
    width = self.adapted_image.shape[1]

    self.show_stats(self.adapted_image)

    # The playfield consists of 18x10 tiles
    tile_height = int(height / self.needed_number_of_tiles_height)
    tile_width = int(width / self.needed_number_of_tiles_width)

    return tile_height, tile_width








