import numpy as np
from PIL import Image, ImageOps, ImageStat
import cv2
from tile_recognizer import TileRecognizer, Tiler
import pytesseract

class GameboyImage():
  """
  Provides standard operations for
  a full or part gameboy screen image
  """
  def __init__(self, image, nr_of_tiles_height, nr_of_tiles_width, tile_height, tile_width, is_tiled=True):
    """
    Image as numpy array.
    """
    self.image = image
    self.is_tiled = is_tiled
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

class PlayfieldRecreator():
  def __init__(self):
    self.tiles = self._load_tiles()

  def recreate(self, playfield_array, path):
    for column_nr, column in enumerate(playfield_array):
      for row_nr, tile_nr in enumerate(column):
        if(tile_nr == -99):
          tile_nr = 12
        tile = self.tiles[tile_nr]
        if(row_nr > 0):
          row = np.concatenate((row,tile), axis=1)
        else:
          row = tile
      if(column_nr > 0):
        result = np.concatenate((result, row), axis=0)
      else:
        result = row

    cv2.imwrite(path, result)

    return result

  def _open_image(self, path):
    return np.array(Image.open(path).convert('RGB'))

  def _load_tiles(self):
    return [
      self._open_image("images/tiles/81.png"), #j
      self._open_image("images/tiles/82.png"), #z
      self._open_image("images/tiles/83.png"), #o
      self._open_image("images/tiles/84.png"), #l
      self._open_image("images/tiles/85.png"), #t
      self._open_image("images/tiles/86.png"), #s

      self._open_image("images/tiles/80.png"), #t1
      self._open_image("images/tiles/88.png"), #t2
      self._open_image("images/tiles/89.png"), #t3
      self._open_image("images/tiles/8A.png"), #t4
      self._open_image("images/tiles/8B.png"), #i5
      self._open_image("images/tiles/8F.png"), #i6

      self._open_image("images/tiles/2F.png"), #white
    ]

class NumberProcessor():
  def __init__(self, image):
    self.original_image = np.array(image)
    self.processed_image = self._add_border(image)
    self.number = self._run()

  def _add_border(self, image_as_array):
    bordered = Image.fromarray(np.array(image_as_array))
    bordered = ImageOps.expand(bordered, border=10, fill='white')
    return np.array(bordered)

  def _run(self):
    return int(self._ocr(self.processed_image))

  def _ocr(self, image):
    # Run tesseract in one-line mode (--psm=6)
    # Use training data specifically trained for tetris numbers
    return pytesseract.image_to_string(image, config=r'--dpi 252 --psm 6 --tessdata-dir .', lang="tetris").strip()

  def get_number(self):
    return self.number

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
          cv2.imwrite('test/tiles/' + str(column_nr) + "-" + str(row_nr) + '-full-view-tile.png', tile)

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

  def run(self):
    result = []

    for column_nr, column in enumerate(self.tiled_image):
      for row_nr, tile in enumerate(column):
        cv2.imwrite('test/tiles/' + str(column_nr) + "-" + str(row_nr) + '-screenshot-tile.png', tile)
        result.append(self.recognizer.recognize(tile))

    return np.array(result).reshape(18, 10)

  def tile_image(self):
    tiler = Tiler(self.needed_number_of_tiles_height, self.needed_number_of_tiles_width, self.original_image)
    return tiler.adapted_image







