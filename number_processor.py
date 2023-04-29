import numpy as np
import pytesseract
from PIL import Image, ImageOps

# Use this if your tesseract excutable is not in PATH
#pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

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
    result = self._ocr(self.processed_image)
    if(result.isdigit()):
      result = int(result)
    else:
      result = None
    return result

  def _ocr(self, image):
    # Run tesseract in one-line mode (--psm=6)
    # Use training data specifically trained for tetris numbers
    return pytesseract.image_to_string(image, config=r'--dpi 252 --psm 6 --tessdata-dir .', lang="tetris").strip()

  def get_number(self):
    return self.number

  def is_digit(self):
    return(not self.number == None)