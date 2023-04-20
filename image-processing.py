import numpy as np
import cv2
from mss import mss
import pytesseract
import time
from PIL import Image, ImageOps
import matplotlib.pyplot as plt
from csvfile import CSVWriter
from retrieve_bounding_box import BoundingBoxWidget

#bounding_box = {'top': 135, 'left': -3025, 'width': 600, 'height': 525}
bounding_box_score = {'top': 220, 'left': 1535, 'width': 180, 'height': 29}
bounding_box_lines = {'top': 415, 'left': 1557, 'width': 135, 'height': 29}
sct = mss()

# Use this if your tesseract excutable is not in PATH
#pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def grab_and_write_image(bounding_box, numbering=0, postfix=""):
  image = grab_image(bounding_box)
  image = add_border(image)
  cv2.imwrite('screenshots/screenshot-' + str(numbering) + postfix + ".png", np.array(image))

def screenshots(times=-1, intervall=1):
  counter = 0
  while counter < times or times==-1:
    grab_and_write_image(bounding_box_lines, numbering=counter, postfix="-lines")
    grab_and_write_image(bounding_box_score, numbering=counter, postfix="-score")
    counter += 1
    time.sleep(intervall)

def grab_and_process_image(bouding_box):
  """
  returns a string
  """
  image = grab_image(bouding_box)
  image = add_border(image)
  #cv2.imwrite(folder + 'screenshot.png', np.array(image))
  result = tess(image)
  return result

def grab_image(bounding_box):
  return sct.grab(bounding_box)

def add_border(image_as_array):
  bordered = Image.fromarray(np.array(image_as_array))
  bordered = ImageOps.expand(bordered, border=10, fill='white')
  return np.array(bordered)

def show_plot(scores, lines):
  plt.scatter(lines, scores)
  plt.savefig(r'plots/test.png')

def run(debug=False):
  csv_file = CSVWriter()
  accepted_score = -1
  accepted_lines = -1
  score_array = []
  lines_array = []

  while True:
    current_score = grab_and_process_image(bounding_box_score)
    current_lines = grab_and_process_image(bounding_box_lines)

    if(debug):
      print(current_score)
      print(current_lines)

    if current_score.isdigit() and current_lines.isdigit() and int(current_score) > accepted_score and int(current_lines) > accepted_lines:
      accepted_lines = int(current_lines)
      accepted_score = int(current_score)
      print("Score: " + str(accepted_score) + " Lines: " + str(accepted_lines))

      csv_file.write(accepted_lines, accepted_lines)
      score_array.append(accepted_score)
      lines_array.append(accepted_lines)

    show_plot(score_array, lines_array)
    time.sleep(1)

    if (cv2.waitKey(1) & 0xFF) == ord('q'):
      cv2.destroyAllWindows()
      break

def tess(image):
  # Run tesseract in one-line mode (--psm=6)
  # Use training data from tetris
  return pytesseract.image_to_string(image, config=r'--dpi 252 --psm 6 --tessdata-dir .', lang="tetris").strip()

if __name__ == "__main__":
  #run()
  screenshots(1)
