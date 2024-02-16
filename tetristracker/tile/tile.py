import cv2
import numpy as np
from PIL import Image, ImageStat


class Tile:
  """
  A tile always gets rescaled to 24x24
  """
  STANDARD_WIDTH = 24
  STANDARD_HEIGHT = 24
  THRESHOLD = 300

  def __init__(self, tile_image, column_nr=None, row_nr=None):
    self.tile_image = np.array(Image.fromarray(tile_image).convert('L').resize((Tile.STANDARD_WIDTH, Tile.STANDARD_HEIGHT), Image.Resampling.BOX))
    self.grey_image = self.tile_image
    self.column_nr = column_nr
    self.row_nr = row_nr

  def store(self, path_and_name):
    cv2.imwrite(path_and_name, self.tile_image)

  def brightness(self):
    """
    From: https://stackoverflow.com/a/7433184
    By: deprecated
    CC BY-SA 3.0
    """
    arr = np.array(self.grey_image, dtype=np.int32)
    rms = np.sqrt(np.mean(np.square(arr)))
    return rms

  def center_brightness(self):
    """
    Tests only the inner third for brightness
    """
    border_width = int(Tile.STANDARD_WIDTH/3)
    border_height = int(Tile.STANDARD_HEIGHT/3)
    arr = np.array(self.grey_image[border_height:Tile.STANDARD_HEIGHT-border_height, border_width:Tile.STANDARD_WIDTH-border_width], dtype=np.int32)
    rms = np.sqrt(np.mean(np.square(arr)))
    return rms

  def is_in_transition(self):
    return not self.is_white() and self.get_min() > Tile.THRESHOLD

  def is_dull(self):
    """
    An image is dull if the difference of
    the whitest pixel and the blackest
    pixel is small.
    For some error correction we remove 5%
    of the whitest and 5% of the blackest
    pixels.
    """
    greyed_image = self.grey_image
    count_of_pixels = greyed_image.shape[0] * greyed_image.shape[1]
    five_percent_of_pixels = int(count_of_pixels*0.05)
    unique_values, unique_count = np.unique(greyed_image, return_counts=True)
    cumulative_sum_forward = np.cumsum(unique_count)
    cumulative_sum_backward = np.flip(np.cumsum(np.flip(unique_count)))
    reduced = unique_values[(cumulative_sum_forward > five_percent_of_pixels) & (cumulative_sum_backward > five_percent_of_pixels)]
    return reduced[-1]-reduced[0] < 75

  def is_black(self):
    """
    Expects a 3D-numpy-array [h, w, 1]

    Every tile that consists of more than
    75% white pixels is considered as black.
    This removes difficult edge cases and
    make template matching slightly more precise
    :return: true if 75% of the tile is black, false otherwise
    """
    image = np.zeros(self.tile_image.shape)
    image[self.tile_image == 0] = 1
    total_number_of_pixels = image.shape[0]*image.shape[1] #w*h
    number_of_black_pixels = np.sum(image)
    return number_of_black_pixels/total_number_of_pixels > 0.75

  def is_one_color(self, threshhold=1):
    """
    Return if the tile consists of mostly (75%)
    one color. Color here means the same grey
    value.
    We take into account close values. Values
    that are max one value away.
    """
    image_sum = self.grey_image
    resolution = image_sum.shape[0] * image_sum.shape[1]
    unique_values, unique = np.unique(image_sum, return_counts=True)
    percent_appearance = unique/resolution
    max_index = np.argmax(percent_appearance)
    max_value = unique_values[max_index]
    res = np.sum( percent_appearance[(unique_values <= max_value + threshhold) & (unique_values >= max_value - threshhold) ])
    return res > 0.75

  def is_white(self, threshhold=0.75):
    """
    Expects a 3D-numpy-array [h, w, 1]

    Standard: Every tile that consists of more than
    75% white pixels is considered as white.
    This removes difficult edge cases and
    make template matching slightly more precise

    You can adjust this value by passing the new
    threshhold value.

    :return: true if at least threshold (standard is 75%) of the tile is white, false otherwise
    """
    image = self.tile_image.copy()
    # set everything not white to 1
    image[image < 255] = 1
    # set everything white to 0
    image[image == 255] = 0
    resolution = image.shape[0]*image.shape[1]
    return np.sum(image)/resolution < (1-threshhold)

  def resize(self, height, width):
    self.tile_image = np.array(Image.fromarray(self.tile_image).resize((width, height), Image.Resampling.LANCZOS))
    return self

  def get_black_or_white_array(self):
    image = np.zeros(shape=self.grey_image.shape)
    image[self.grey_image > 127] = 1
    return image

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
