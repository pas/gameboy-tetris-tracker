import numpy as np
from PIL import Image


class Tiler:
  def __init__(self, nr_tiles_height, nr_tiles_width, image):
    self.nr_tiles_height = nr_tiles_height
    self.nr_tiles_width = nr_tiles_width
    self.original_image = image
    self._tile()

    # adapted image height and width in pixel
    self.image_height = self.adapted_image.shape[0]
    self.image_width = self.adapted_image.shape[1]

    # tile height and width in pixel
    self.tile_height = int(self.image_height / self.nr_tiles_height)
    self.tile_width = int(self.image_width / self.nr_tiles_width)

    self.adapted_image = self._tile_image()

  def _tile_image(self):
    last_dimension = self.adapted_image.shape[-1]
    return self.adapted_image.reshape(self.nr_tiles_height, self.tile_height,
                                      self.nr_tiles_width, self.tile_width, last_dimension).swapaxes(1, 2)

  def _tile(self):
    """
    Returns the tiled image. Resizes image
    to fit to a proper tiling (every piece
    the same size). The size of the image
    before and after will therefore in many
    cases be different. Expects image as
    numpy array.
    """
    shape = self.original_image.shape
    height = shape[0]
    width = shape[1]

    even_height = height % self.nr_tiles_height
    even_width = width % self.nr_tiles_width

    new_height = height + self.nr_tiles_height - even_height
    new_width = width + self.nr_tiles_width - even_width

    self.adapted_image = self.original_image.copy()

    if(even_width > 0 or even_height > 0):
      self.adapted_image =  np.array(Image.fromarray(self.adapted_image).resize((new_width, new_height), Image.Resampling.BILINEAR))

    even_height = self.adapted_image.shape[0] % self.nr_tiles_height
    even_width = self.adapted_image.shape[1] % self.nr_tiles_width

    assert(even_height == 0)
    assert(even_width == 0)
