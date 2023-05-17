import cv2


class GameboyImage():
  """
  Provides standard operations for
  a full or part gameboy screen image
  """
  def __init__(self, image, nr_of_tiles_height=None, nr_of_tiles_width=None, tile_height=None, tile_width=None, is_tiled=True):
    """
    Image as numpy array.
    """
    self.image = image
    self.is_tiled = is_tiled
    if(is_tiled):
      self.nr_of_tiles_height = image.shape[0]
      self.nr_of_tiles_width = image.shape[1]
      self.tile_width = image.shape[2]
      self.tile_height = image.shape[3]
    else:
      self.nr_of_tiles_height = nr_of_tiles_height
      self.nr_of_tiles_width = nr_of_tiles_width
      self.tile_height = tile_height
      self.tile_width = tile_width

  def tile(self):
    """
    Tiles the image and returns it.
    """
    if(not self.is_tiled):
      self.image = self._tile()
      self.is_tiled = True

    return self.image

  def _tile(self):
    last_dimension = self.image.shape[-1]
    return self.image.reshape(self.nr_of_tiles_height, self.tile_height,
                                      self.nr_of_tiles_width, self.tile_width, last_dimension).swapaxes(1, 2)

  def untile(self):
    """
    Untiles the image and returns it.
    """
    if(self.is_tiled):
      self.image = self._untile()
      self.is_tiled = False

    return self.image

  def _untile(self):
    shape = self.image.shape
    nr_of_tiles_height = shape[0]
    nr_of_tiles_width = shape[1]
    tile_width = shape[2]
    tile_height = shape[3]
    color_channels = shape[4]
    return self.image.swapaxes(1, 2).reshape(nr_of_tiles_height * tile_height, nr_of_tiles_width * tile_width,
                                        color_channels)

  def save(self, path="", name="image", extension="png"):
    if(not self.is_tiled):
      cv2.imwrite(path + name + "." + extension, self.image)
    else:
      for column_nr, column in enumerate(self.image):
        for row_nr, tile in enumerate(column):
            cv2.imwrite(path + str(column_nr) + "-" + str(row_nr) + '-' + name + '.' + extension, tile)