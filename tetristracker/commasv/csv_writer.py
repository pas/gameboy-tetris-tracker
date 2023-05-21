import csv
import datetime


class CSVWriter:
  headers = ["time", "score", "lines", "level", "preview", "playfield"]

  def __init__(self, path="csv/", file_name="results.csv"):
    prefix = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    self.file_name = path + prefix + "-" + file_name
    self._write(self.headers[1], self.headers[2], self.headers[0], self.headers[3], self.headers[4], self.headers[5])

  def write(self, score, lines, level, preview, playfield):
    """
    Expects a numpy array as playfield
    """
    time = datetime.datetime.now()
    self._write(score, lines, level, time.strftime("%Y/%m/%d %H:%M:%S.%f"), preview, playfield.tolist())

  def _write(self, score, lines, level, time, preview, playfield):
    with open(self.file_name, 'a+', newline='') as csv_file:
      csv_writer = csv.writer(csv_file, delimiter=";")
      csv_writer.writerow([time, score, lines, level, preview, playfield])
