import datetime
import sqlite3
import json

from tetristracker.commasv.writer import Writer


class SqliteWriter(Writer):
  def __init__(self, path="screenshots/", file_name="tetris.db"):
    self.con = sqlite3.connect(path + file_name)
    self.con.execute("CREATE TABLE IF NOT EXISTS rounds(id INTEGER PRIMARY KEY, "
                     "round_id INTEGER, "
                     "time TEXT, "
                     "score INTEGER, "
                     "lines INTEGER, "
                     "level INTEGER, "
                     "preview INTEGER, "
                     "spawned BOOLEAN, "
                     "playfield TEXT);")
    self.id = int(datetime.datetime.now().strftime("%Y%m%d%H%M%S"))

  def write(self, score : int, lines : int, level : int, preview : int, spawned : bool, playfield):
    """
    Expects a numpy array as playfield
    """
    time = datetime.datetime.now()
    self._write(score, lines, level, time.strftime("%Y/%m/%d %H:%M:%S.%f"), preview, spawned, playfield.tolist())

  def _write(self, score : int, lines : int, level : int, time : datetime.datetime, preview : int, spawned : bool, playfield):
    command = "INSERT INTO rounds (round_id, time, score, lines, level, preview, spawned, playfield) VALUES (" + self._create_sqlite_string(score, lines, level, time, preview, spawned, playfield) + ")"
    self.con.execute(command)
    self.con.commit()

  def _create_sqlite_string(self, score, lines, level, time, preview, spawned, playfield):
    return str(self.id) + "," + \
            "\'" + time + "\'," + \
            str(score) + "," + \
            str(lines) + "," + \
            str(level) + "," + \
            str(preview) + "," + \
            str(spawned) + "," + \
            "\'" + json.dumps(playfield) + "\'"