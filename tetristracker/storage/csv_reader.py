import datetime

import numpy as np

import csv

from tetristracker.image.playfield_recreator import PlayfieldRecreator


class CSVReader:
  TIME = 0
  SCORE = 1
  LINES = 2
  LEVEL = 3
  PREVIEW = 4
  PLAYFIELD = 5

  headers = ["time", "score", "lines", "preview", "playfield"]

  def __init__(self, prefix, path="csv/", file_name="results.csv"):
    self.prefix = prefix
    self.file_name = file_name
    self.path = path
    self.recreator = PlayfieldRecreator()
    self.delimiter = ";"

  def set_delimiter(self, delimiter):
    self.delimiter = delimiter

  def get_full_path(self):
    return self.path + self.prefix + "-" + self.file_name

  def get_lines_and_scores(self):
    lines = []
    scores = []

    with open(self.get_full_path(), newline='') as csv_file:
      reader = csv.reader(csv_file, delimiter=self.delimiter)
      next(reader)
      for row in reader:
        lines.append(int(row[CSVReader.LINES]))
        scores.append(int(row[CSVReader.SCORE]))

    return lines, scores

  def to_image(self, path):
    """
    Takes the given csv and recreates the playfields
    as images
    """
    with open(self.get_full_path(), newline='') as csv_file:
      reader = csv.reader(csv_file, delimiter=";")
      next(reader)
      for row in reader:
        playfield = eval(row[CSVReader.PLAYFIELD])
        row[0] = datetime.datetime.strptime(row[0], "%Y/%m/%d %H:%M:%S.%f")
        self.recreator.recreate(np.array(playfield), path + str(row[0].timestamp() * 1000) + ".png")
