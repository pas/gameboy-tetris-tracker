import numpy as np
import cv2
from mss import mss
import pytesseract
import time
from PIL import Image, ImageOps
import matplotlib.pyplot as plt
from csvfile import CSVWriter
import yaml
import calculations

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

  def add_slope(self, slope, ax):
    x_min, x_max = ax.get_xlim()
    y_min, y_max = 0, slope * (x_max - x_min)
    ax.plot([x_min, x_max], [y_min, y_max])
    ax.set_xlim([x_min, x_max])

  def get_limits(self, current_max_score, current_max_lines):
    score = 1000

    # the uglier the better...
    if current_max_score > 1000:
      score = 10000
    if current_max_score > 10000:
      score = 100000
    if current_max_score > 100000:
      score = 500000
    if current_max_score > 500000:
      score = 999999

    lines = 10
    if current_max_lines > 10:
      lines = 50
    if current_max_lines > 50:
      lines = 100
    if current_max_lines > 100:
      lines = 150
    if current_max_lines > 150:
      lines = 200
    if current_max_lines > 200:
      lines = 250
    if current_max_lines > 250:
      lines = 300

    return score, lines

  def show_plot(self, scores, lines):
    if(len(scores) > 3):
      fig, ax = plt.subplots()
      ax.scatter(lines, scores)
      top, right = self.get_limits(scores[len(scores)-1], lines[len(lines)-1])
      ax.set_xlim(left=0, right=right)
      ax.set_ylim(bottom=0, top=top)
      slope = calculations.get_slope(lines, scores)
      self.add_slope(slope, ax)

      fig.savefig(r'plots/test.png')

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
