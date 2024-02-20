import datetime
import json
import sqlite3

import numpy as np

import csv

from tetristracker.image.playfield_recreator import PlayfieldRecreator
from tetristracker.unit.round_values import RoundValues


class SqliteReader:
  ID = 0
  ROUND_ID = 1
  TIME = 2
  SCORE = 3
  LINES = 4
  LEVEL = 5
  PREVIEW = 6
  TETROMINO_IN_PLAY = 7
  SPAWNED = 8
  PLAYFIELD = 9

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
      entry[self.PLAYFIELD] = json.loads(entry[self.PLAYFIELD])
      entry[self.TIME] = datetime.datetime.strptime(entry[self.TIME], "%Y/%m/%d %H:%M:%S.%f")
    return res

  def get_all(self):
    return self.values

  def get_start_and_end_times_per_round(self):
    query = "SELECT round_id, MIN(time) AS start, MAX(time) AS end FROM rounds GROUP BY round_id"
    res = self.connect_and_execute(query)
    res = self._deserialize_start_and_end_times(res)
    return res

  def connect_and_execute(self, query):
    con = sqlite3.connect(self.path + self.file_name)
    res = con.execute(query)
    return self._to_list(res.fetchall())

  def get_round_ids(self):
    query = "SELECT DISTINCT round_id FROM rounds"
    res = self.connect_and_execute(query)
    return res

  def get_round(self, round_id):
    query = "SELECT * FROM rounds WHERE round_id = "+round_id+";"
    res = self.connect_and_execute(query)
    res = self._deserialize_round(res)
    return res

  def _deserialize_round(self, values):
    for round in values:
      round[self.TIME] = datetime.datetime.strptime(round[self.TIME], "%Y/%m/%d %H:%M:%S.%f")
      round[self.PLAYFIELD] = json.loads(round[self.PLAYFIELD])
    return values

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
