import numpy as np
import cv2
from mss import mss
import pytesseract
import time
from PIL import Image, ImageOps
import matplotlib.pyplot as plt
from csvfile import CSVWriter
import yaml

# Use this if your tesseract excutable is not in PATH
#pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

class Runner:
  bounding_box_score = ""
  bounding_box_lines = ""
  sct = ""
  configs = ""

  def __init__(self, config_file="config.yml"):
    self.sct = mss()
    with open('config.yml', 'r') as config_file:
      self.configs = yaml.safe_load(config_file)
      self.bounding_box_lines = self.configs["lines"]["bounding_box"]
      self.bounding_box_score = self.configs["score"]["bounding_box"]

  def grab_and_process_image(self, bouding_box):
    """
    returns a string
    """
    image = self.grab_image(bouding_box)
    image = self.add_border(image)
    #cv2.imwrite(folder + 'screenshot.png', np.array(image))
    result = self.tess(image)
    return result

  def grab_image(self, bounding_box):
    return self.sct.grab(bounding_box)

  def add_border(self, image_as_array):
    bordered = Image.fromarray(np.array(image_as_array))
    bordered = ImageOps.expand(bordered, border=10, fill='white')
    return np.array(bordered)

  def show_plot(self, scores, lines):
    plt.scatter(lines, scores)
    plt.savefig(r'plots/test.png')

  def run(self, debug=False):
    csv_file = CSVWriter()
    accepted_score = -1
    accepted_lines = -1
    score_array = []
    lines_array = []

    while True:
      current_score = self.grab_and_process_image(self.bounding_box_score)
      current_lines = self.grab_and_process_image(self.bounding_box_lines)

      if(debug):
        print(current_score)
        print(current_lines)

      if current_score.isdigit() and current_lines.isdigit() and int(current_score) > accepted_score and int(current_lines) > accepted_lines:
        accepted_lines = int(current_lines)
        accepted_score = int(current_score)
        print("Score: " + str(accepted_score) + " Lines: " + str(accepted_lines))

        csv_file.write(accepted_score, accepted_lines)
        score_array.append(accepted_score)
        lines_array.append(accepted_lines)

      self.show_plot(score_array, lines_array)
      time.sleep(1)

      if (cv2.waitKey(1) & 0xFF) == ord('q'):
        cv2.destroyAllWindows()
        break

  def tess(self, image):
    # Run tesseract in one-line mode (--psm=6)
    # Use training data from tetris
    return pytesseract.image_to_string(image, config=r'--dpi 252 --psm 6 --tessdata-dir .', lang="tetris").strip()

if __name__ == "__main__":
  runner = Runner()
  runner.run()
