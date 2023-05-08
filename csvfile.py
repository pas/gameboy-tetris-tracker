import datetime
import csv
from playfield_recreator import PlayfieldRecreator
import numpy as np

class CSVReader:
  headers = ["time", "score", "lines", "preview", "playfield"]

  def __init__(self, prefix, path="csv/", file_name="results.csv"):
    self.prefix = prefix
    self.file_name = file_name
    self.path = path
    self.recreator = PlayfieldRecreator()

  def get_full_path(self):
    return self.path + self.prefix + "-" + self.file_name

  def to_image(self, path):
    """
    Takes the given csv and recreates the playfields
    as images
    """
    with open(self.get_full_path(), newline='') as csv_file:
      reader = csv.reader(csv_file, delimiter=";")
      next(reader)
      for row in reader:
        playfield = eval(row[4])
        row[0] = datetime.datetime.strptime(row[0], "%Y/%m/%d %H:%M:%S.%f")
        self.recreator.recreate(np.array(playfield), path + str(row[0].timestamp() * 1000) + ".png")

class CSVWriter:
  headers = ["time", "score", "lines", "preview", "playfield"]

  def __init__(self, path="csv/", file_name="results.csv"):
    prefix = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    self.file_name = path + prefix + "-" + file_name
    self._write(self.headers[1], self.headers[2], self.headers[0], self.headers[3], self.headers[4])

  def write(self, score, lines, preview, playfield):
    """
    Expects a numpy array as playfield
    """
    time = datetime.datetime.now()
    self._write(score, lines, time.strftime("%Y/%m/%d %H:%M:%S.%f"), preview, playfield.tolist())

  def _write(self, score, lines, time, preview, playfield):
    with open(self.file_name, 'a+', newline='') as csv_file:
      csv_writer = csv.writer(csv_file, delimiter=";")
      csv_writer.writerow([time, score, lines, preview, playfield])