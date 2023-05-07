import numpy as np
import cv2
from mss import mss
import pytesseract
import time
from PIL import Image, ImageOps
import yaml
from gameboy_view_processor import GameboyViewProcessor
from capturer import MSSCapturer


# Use this if your tesseract excutable is not in PATH
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

class Check:
  def __init__(self, config_file="config.yml"):
    with open('config.yml', 'r') as config_file:
      self.configs = yaml.safe_load(config_file)
      self.bounding_box = self.configs["bounding_box"]
      self.capturer = MSSCapturer(self.bounding_box)



  def grab_and_write_image(self, numbering=0, postfix=""):
    image = self.capturer.grab_image()
    GameboyViewProcessor(image, save_tiles=True)
    image = self.add_border(image)

    cv2.imwrite('screenshots/screenshot-' + str(numbering) + postfix + ".png", np.array(image))

  def screenshots(self, times=-1, intervall=1):
    self.check_width_and_length()
    counter = 0
    while counter < times or times==-1:
      self.grab_and_write_image(numbering=counter)
      counter += 1
      time.sleep(intervall)

  def check_width_and_length(self):
    """
    Should be dividable by 18 in height
    and by 20 in width
    """
    print("Modulo width: " + str(self.bounding_box["width"] % 20))
    print("Modulo height: " + str(self.bounding_box["height"] % 18))

  def add_border(self, image_as_array):
    bordered = Image.fromarray(np.array(image_as_array))
    bordered = ImageOps.expand(bordered, border=10, fill='blue')
    return np.array(bordered)

if __name__ == "__main__":
  check = Check()
  check.screenshots(1)
