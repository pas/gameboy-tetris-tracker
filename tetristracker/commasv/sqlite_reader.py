import datetime
import json
import sqlite3

import numpy as np

import csv

from tetristracker.image.playfield_recreator import PlayfieldRecreator
from tetristracker.unit.round_values import RoundValues


class SqliteReader:
  TIME = 0
  SCORE = 1
  LINES = 2
  LEVEL = 3
  PREVIEW = 4
  PLAYFIELD = 5

  headers = ["time", "score", "lines", "preview", "playfield"]

  def __init__(self, prefix="", path="screenshots/", file_name="tetris.db"):
    self.prefix = prefix
    self.file_name = file_name
    self.path = path
    self.values = self._get_values_from_database(prefix)
    self.recreator = PlayfieldRecreator()

  def _to_list(self, sqlite_fetchall):
    return [list(entry) for entry in sqlite_fetchall]

  def _get_values_from_database(self, prefix=""):
    con = sqlite3.connect(self.path + self.file_name)
    res = con.execute("SELECT * FROM rounds WHERE round_id = '" + prefix + "';")
    res = res.fetchall()
    res = self._to_list(res)
    for entry in res:
      entry[7] = json.loads(entry[7])
      entry[1] = datetime.datetime.strptime(entry[2], "%Y/%m/%d %H:%M:%S.%f")
    return res

  def get_all(self):
    return self.values

  def get_start_and_end_times_per_round(self):
    query = "SELECT round_id, MIN(time) AS start, MAX(time) AS end FROM rounds GROUP BY round_id"
    con = sqlite3.connect(self.path + self.file_name)
    res = con.execute(query)
    res = self._to_list(res.fetchall())
    res = self._deserialize_start_and_end_times(res)
    return res

  def _deserialize_start_and_end_times(self, values):
    result = []
    for round in values:
      start = datetime.datetime.strptime(round[1], "%Y/%m/%d %H:%M:%S.%f")
      end = datetime.datetime.strptime(round[2], "%Y/%m/%d %H:%M:%S.%f")
      round_values = RoundValues(start,
                                 end,
                                 end-start)
      result.append(round_values)

    return result

  def get_lines_and_scores(self):
    pass

  def to_image(self, path):
    pass
