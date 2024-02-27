from tetristracker.storage.csv_writer import CSVWriter
from tetristracker.storage.sqlite_writer import SqliteWriter


class StorageSelection:
  def __init__(self):
    self.storage = None
    self.name = ""

  def get(self):
    return self.storage

  def select(self, name):
    if(name == "sqlite"):
      self.select_sqlite()
    if(name == "csv"):
      self.select_csv()

  def select_sqlite(self):
    self.name = "sqlite"
    self.storage = SqliteWriter()

  def select_csv(self):
    self.name = "csv"
    self.plotter = CSVWriter()