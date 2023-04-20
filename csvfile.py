import datetime
import csv

class CSVWriter:
  headers = ["time", "score", "lines"]
  file_name = ""

  def __init__(self, file_name="csv/results.csv"):
    self.file_name = file_name
    self._write(self.headers[1], self.headers[2], self.headers[0])

  def write(self, score, lines, time=datetime.datetime.now()):
    """
    Expects a datetime object
    """
    self._write(score, lines, time.strftime("%Y/%m/%d %H:%M:%S"))

  def _write(self, score, lines, time):
    with open(self.file_name, 'a+', newline='') as csv_file:
      csv_writer = csv.writer(csv_file)
      csv_writer.writerow([time, score, lines])