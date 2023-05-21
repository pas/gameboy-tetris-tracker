import numpy as np
from PIL import Image, ImageStat
import cv2


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

class TetrominoTransmission:
  # values turn clockwise

  # l lays flat facing down
  L_TETROMINO = 0
  L_TETROMINO_90 = 1
  L_TETROMINO_180 = 2
  L_TETROMINO_270 = 3
  # j lays flat facing down
  J_TETROMINO = 4
  J_TETROMINO_90 = 5
  J_TETROMINO_180 = 6
  J_TETROMINO_270 = 7
  # i lays flat
  I_TETROMINO = 8
  I_TETROMINO_90 = 9
  # z lays flat (three pieces wide)
  Z_TETROMINO = 10
  Z_TETROMINO_90 = 11
  # s lays flat (three pieces wide)
  S_TETROMINO = 14
  S_TETROMINO_90 = 15
  # t lays flat facing down
  T_TETROMINO = 18
  T_TETROMINO_90 = 19
  T_TETROMINO_180 = 20
  T_TETROMINO_270 = 21
  # o is just o ;)
  O_TETROMINO = 22

class Tetromino:
  @staticmethod
  def get_surface_array_l1():
    return [[TetrominoTransmission.L_TETROMINO_270, TetrominoTransmission.O_TETROMINO, TetrominoTransmission.J_TETROMINO_90],
            [TetrominoTransmission.Z_TETROMINO_90, TetrominoTransmission.T_TETROMINO_270],
            [TetrominoTransmission.J_TETROMINO_270],
            [TetrominoTransmission.L_TETROMINO_90],
            [TetrominoTransmission.S_TETROMINO_90, TetrominoTransmission.T_TETROMINO_90]]

  @staticmethod
  def get_surface_array_l2():
    return [[ [TetrominoTransmission.L_TETROMINO_180, TetrominoTransmission.J_TETROMINO_180, TetrominoTransmission.T_TETROMINO_180],
              [TetrominoTransmission.S_TETROMINO],
              [TetrominoTransmission.J_TETROMINO]],
            [ [TetrominoTransmission.L_TETROMINO], [], []],
            [ [], [], []],
            [ [], [], []],
            [ [TetrominoTransmission.Z_TETROMINO],
              [TetrominoTransmission.T_TETROMINO], []]]



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

class TileRecognizer:
  J_MINO = 0
  Z_MINO = 1
  O_MINO = 2
  L_MINO = 3
  T_MINO = 4
  S_MINO = 5
  I_MINO_SIMPLE = 6
  GREY = 12
  EMPTY = -99

  def __init__(self,):
    self.mino_array = self.create_mino_array()

  def recognize(self, tile, simplify_i_mino=False):
    """
    :param tile:
    :param simplify_t_mino: Replaces all found T-minos
    with the value of T_MINO_SIMPLE
    :return:
    """
    best_match = -99 # default is a white tile
    tile = Tile(tile)

    # Skip white tiles
    if (not tile.is_white()):
      template_matching_values = self.matching(tile.tile_image)
      best_match = np.argmax(template_matching_values)

      if(simplify_i_mino and best_match > TileRecognizer.I_MINO_SIMPLE):
        best_match = TileRecognizer.I_MINO_SIMPLE

      # Seems to be difficult for template matching
      # to correctly identify the L piece. Checking
      # for brightness and only decide between
      # L-Mino and S-Mino should help
      # We are looking for white in center
      if (tile.brightness() < 95):
        # The center of the S-Mino is bright
        if(tile.center_brightness() > 100):
          best_match = TileRecognizer.S_MINO
        else:
          best_match = TileRecognizer.L_MINO


    return best_match

  def matching(self, tile):
    methods = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR',
               'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']

    result = []
    for mino_template in self.mino_array:
      match_value = cv2.matchTemplate(tile, mino_template, eval(methods[0]))
      result.append(match_value)

    return np.array(result).flatten()

  def retrieve_template(self, path):
    image = Image.open(path).convert('RGB').resize((Tile.STANDARD_WIDTH, Tile.STANDARD_HEIGHT), Image.Resampling.BILINEAR)
    return np.array(image)

  def create_mino_array(self):
    j_mino = self.retrieve_template("../../images/tiles/81.png")
    z_mino = self.retrieve_template("../../images/tiles/82.png")
    o_mino = self.retrieve_template("../../images/tiles/83.png")
    l_mino = self.retrieve_template("../../images/tiles/84.png")
    t_mino = self.retrieve_template("../../images/tiles/85.png")
    s_mino = self.retrieve_template("../../images/tiles/86.png")

    t1_mino = self.retrieve_template("../../images/tiles/80.png")
    t2_mino = self.retrieve_template("../../images/tiles/88.png")
    t3_mino = self.retrieve_template("../../images/tiles/89.png")
    t1r_mino = self.retrieve_template("../../images/tiles/8A.png")
    t2r_mino = self.retrieve_template("../../images/tiles/8B.png")
    t3r_mino = self.retrieve_template("../../images/tiles/8F.png")

    #This needs to be in the same order as the names
    return [
            j_mino,                 z_mino,               o_mino,                 l_mino,                   t_mino,
            s_mino,                 t1_mino,              t2_mino,                t3_mino,                  t1r_mino,
            t2r_mino,               t3r_mino,]
            #edge_case_border_left,  edge_case_border_bottom,  edge_case_border_right, edge_case_border_top]