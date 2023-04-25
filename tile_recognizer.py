import numpy as np
from PIL import Image, ImageOps, ImageStat
import cv2

class Tile:
  """
  A tile always gets rescaled to 24x24
  """
  STANDARD_WIDTH = 24
  STANDARD_HEIGHT = 24

  def __init__(self, tile_image):
    self.tile_image = np.array(Image.fromarray(tile_image).convert('RGB').resize((Tile.STANDARD_WIDTH,Tile.STANDARD_HEIGHT), Image.Resampling.BILINEAR))
    self._white_to_black_border()

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

class TileRecognizer:
  J_MINO = 0
  Z_MINO = 1
  O_MINO = 2
  L_MINO = 3
  T_MINO = 4
  S_MINO = 5

  def __init__(self,):
    self.mino_array = self.create_mino_array()

  def recognize(self, tile):
    best_match = -99 # default is a white tile
    tile = Tile(tile)

    # Skip white tiles
    if (not tile.is_white()):
      template_matching_values = self.matching(tile.tile_image)
      best_match = np.argmax(template_matching_values)
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
    j_mino = self.retrieve_template("images/tiles/81.png")
    z_mino = self.retrieve_template("images/tiles/82.png")
    o_mino = self.retrieve_template("images/tiles/83.png")
    l_mino = self.retrieve_template("images/tiles/84.png")
    t_mino = self.retrieve_template("images/tiles/85.png")
    s_mino = self.retrieve_template("images/tiles/86.png")

    t1_mino = self.retrieve_template("images/tiles/80.png")
    t2_mino = self.retrieve_template("images/tiles/88.png")
    t3_mino = self.retrieve_template("images/tiles/89.png")
    t1r_mino = self.retrieve_template("images/tiles/8A.png")
    t2r_mino = self.retrieve_template("images/tiles/8B.png")
    t3r_mino = self.retrieve_template("images/tiles/8F.png")

    #This needs to be in the same order as the names
    return [
            j_mino,                 z_mino,               o_mino,                 l_mino,                   t_mino,
            s_mino,                 t1_mino,              t2_mino,                t3_mino,                  t1r_mino,
            t2r_mino,               t3r_mino,]
            #edge_case_border_left,  edge_case_border_bottom,  edge_case_border_right, edge_case_border_top]