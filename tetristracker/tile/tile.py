import cv2
import numpy as np
from PIL import Image, ImageStat


class Tile:
  """
  A tile always gets rescaled to 24x24
  """
  STANDARD_WIDTH = 24
  STANDARD_HEIGHT = 24

  def __init__(self, tile_image, column_nr=None, row_nr=None):
    self.tile_image = np.array(Image.fromarray(tile_image).convert('RGB').resize((Tile.STANDARD_WIDTH, Tile.STANDARD_HEIGHT), Image.Resampling.BOX))
    #self._white_to_black_border()
    self.column_nr = column_nr
    self.row_nr = row_nr

  def store(self, path_and_name):
    cv2.imwrite(path_and_name, self.tile_image)

  def _white_to_black_border(self):
    """
    Checks if image has white borders and recolors
    them to black
    """
    image = self.tile_image
    left_border = image[:,:1]
    #right_border = image[:, :-1]
    left_border[left_border==255] = 0
    #right_border[right_border==255] = 0

  def brightness(self):
    """
    From: https://stackoverflow.com/a/3498247
    By: cmcginty
    CC-BY
    """
    im = Image.fromarray(self.tile_image).convert('L')
    stat = ImageStat.Stat(im)
    return stat.rms[0]

  def center_brightness(self):
    """
    Tests only the inner third for brightness
    """
    border_width = int(Tile.STANDARD_WIDTH/3)
    border_height = int(Tile.STANDARD_HEIGHT/3)
    im = Image.fromarray(self.tile_image[border_height:Tile.STANDARD_HEIGHT-border_height, border_width:Tile.STANDARD_WIDTH-border_width]).convert('L')
    stat = ImageStat.Stat(im)
    return stat.rms[0]

  def is_dull(self):
    """
    An image is dull if the difference of
    the whitest pixel and the blackest
    pixel is small.
    For some error correction we remove 5%
    of the whitest and 5% of the blackest
    pixels.
    """
    greyed_image = np.array(Image.fromarray(self.tile_image).convert('L'))
    count_of_pixels = greyed_image.shape[0] * greyed_image.shape[1]
    five_percent_of_pixels = int(count_of_pixels*0.05)
    unique_values, unique_count = np.unique(greyed_image, return_counts=True)
    cumulative_sum_forward = np.cumsum(unique_count)
    cumulative_sum_backward = np.flip(np.cumsum(np.flip(unique_count)))
    reduced = unique_values[(cumulative_sum_forward > five_percent_of_pixels) & (cumulative_sum_backward > five_percent_of_pixels)]
    return reduced[-1]-reduced[0] < 75

  def is_black(self):
    """
    Expects a 3D-numpy-array [h, w, 3(rgb)]

    Every tile that consists of more than
    75% white pixels is considered as white.
    This removes difficult edge cases and
    make template matching slightly more precise
    :return: true if 75% of the tile is white, false otherwise
    """
    image_sum = np.sum(self.tile_image, axis=-1)
    image = np.zeros(image_sum.shape)
    image[image_sum == 0] = 1
    resolution = image.shape[0]*image.shape[1]
    return np.sum(image)/resolution > 0.75

  def is_one_color(self, threshhold=1):
    """
    Return if the tile consists of mostly (75%)
    one color. Color here means the same grey
    value.
    We take into account close values. Values
    that are max one value away.
    """
    image_sum = np.array(Image.fromarray(self.tile_image).convert('L'))
    resolution = image_sum.shape[0] * image_sum.shape[1]
    unique_values, unique = np.unique(image_sum, return_counts=True)
    percent_appearance = unique/resolution
    max_index = np.argmax(percent_appearance)
    max_value = unique_values[max_index]
    res = np.sum( percent_appearance[(unique_values <= max_value + threshhold) & (unique_values >= max_value - threshhold) ])
    return res > 0.75

  def is_white(self):
    """
    Expects a 3D-numpy-array [h, w, 3(rgb)]

    Every tile that consists of more than
    75% white pixels is considered as white.
    This removes difficult edge cases and
    make template matching slightly more precise
    :return: true if 75% of the tile is white, false otherwise
    """
    image = self.tile_image.copy()
    # set everything not white to 1
    image[image < 255] = 1
    # set everything white to 0
    image[image == 255] = 0
    resolution = image.shape[0]*image.shape[1]*image.shape[2]
    return np.sum(image)/resolution < 0.25

  def resize(self, height, width):
    self.tile_image = np.array(Image.fromarray(self.tile_image).resize((width, height), Image.Resampling.LANCZOS))
    return self

  def get_max(self):
    return np.argmax(np.sum(self.tile_image, axis=-1))

  def get_min(self):
    """
    Sums each pixel up an returns the minimum
    value. More or less the value of the darkest
    pixel.
    """
    sum = np.sum(self.tile_image, axis=-1).flatten()
    res = np.argmin(sum)
    return sum[res]
