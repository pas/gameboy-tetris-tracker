from abc import abstractmethod, ABC

import numpy as np
import pytesseract
from PIL import Image, ImageOps

from tetristracker.tile.tile import Tile


# Use this (with appropriate path) if your tesseract excutable is not in PATH
#pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

class OCRProcessor(ABC):
  def __init__(self, image):
    self.original_image = np.array(image)
    self.processed_image = self._add_border(image)
    self.number = self._run()

  def _run(self):
    result = self._ocr(self.processed_image)
    if(result.isdigit()):
      result = int(result)
    else:
      result = None
    return result

  @abstractmethod
  def _ocr(self):
    pass

  def get_number(self):
    return self.number

  def is_digit(self):
    return self.number != None

  def _add_border(self, image_as_array):
    bordered = Image.fromarray(np.array(image_as_array))
    bordered = ImageOps.expand(bordered, border=10, fill='white')
    return np.array(bordered)

class DigitProcessor(OCRProcessor):
  """
  Processes single digit numbers
  """
  def _ocr(self, image):
    # Run tesseract in one char mode (--psm=10)
    # Use training data specifically trained for tetris numbers
    return pytesseract.image_to_string(image, config=r'--dpi 252 --psm 10 --tessdata-dir .', lang="tetris").strip()

class SequentialNumberProcessor(OCRProcessor):
  def __init__(self, image):
    """
    Expects a tiled image with
    one row and multiple columns
    """
    super().__init__(image)

  def _add_border(self, image_as_array):
    """
    Don't want to do anything here!
    """
    return image_as_array

  def _ocr(self, image):
    number_string = ""
    for tile_image in image[0]:
      tile = Tile(tile_image)
      if not tile.is_white(threshhold=0.77):
        processor = DigitProcessor(tile_image)
        number_string += str(processor.get_number())

    return number_string

class NumberProcessor(OCRProcessor):
  """
  Processes images holding numbers
  with one or more digits
  This is actually not used anymore.
  We are only using the SequentialNumberProcessor
  """
  def _ocr(self, image):
    # Run tesseract in single word mode (--psm=8)
    # Use training data specifically trained for tetris numbers
    return pytesseract.image_to_string(image, config=r'--dpi 252 --psm 8 --tessdata-dir .', lang="tetris-old").strip()