import numpy as np
import cv2
from mss import mss
import pytesseract
import time
from PIL import Image, ImageOps
import yaml


# Use this if your tesseract excutable is not in PATH
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

class Check:
  bounding_box_score = ""
  bounding_box_lines = ""
  bounding_box_playfield = ""
  sct = ""
  configs = ""

  def __init__(self, config_file="config.yml"):
    self.sct = mss()
    with open('config.yml', 'r') as config_file:
      self.configs = yaml.safe_load(config_file)
      self.bounding_box_lines = self.configs["lines"]["bounding_box"]
      self.bounding_box_score = self.configs["score"]["bounding_box"]
      self.bounding_box_playfield = self.configs["playfield"]["bounding_box"]

  def grab_and_write_image(self, bounding_box, numbering=0, postfix=""):
    image = self.grab_image(bounding_box)
    image = self.add_border(image)
    cv2.imwrite('screenshots/screenshot-' + str(numbering) + postfix + ".png", np.array(image))

  def screenshots(self, times=-1, intervall=1):
    counter = 0
    while counter < times or times==-1:
      self.grab_and_write_image(self.bounding_box_lines, numbering=counter, postfix="-lines")
      self.grab_and_write_image(self.bounding_box_score, numbering=counter, postfix="-score")
      self.grab_and_write_image(self.bounding_box_playfield, numbering=counter, postfix="-playfield")
      counter += 1
      time.sleep(intervall)

  def grab_image(self, bounding_box):
    return self.sct.grab(bounding_box)

  def add_border(self, image_as_array):
    bordered = Image.fromarray(np.array(image_as_array))
    bordered = ImageOps.expand(bordered, border=10, fill='white')
    return np.array(bordered)

  def tess(self, image):
    # Run tesseract in one-line mode (--psm=6)
    # Use training data from tetris
    return pytesseract.image_to_string(image, config=r'--dpi 252 --psm 6 --tessdata-dir .', lang="tetris").strip()

if __name__ == "__main__":
  check = Check()
  check.screenshots(1)
