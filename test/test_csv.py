import unittest

from tetristracker.storage.csv_reader import CSVReader


class TestCSV(unittest.TestCase):
  def test_csvreader(self):
    reader = CSVReader("20230511110411", path="test/csv/")
    reader.to_image("test/recreation/")