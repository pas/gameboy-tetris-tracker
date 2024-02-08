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
                     "tetromino_in_play INTEGER, "
                     "spawned BOOLEAN, "
                     "playfield TEXT);")
    self.id = self._create_id()

  def _create_id(self):
    return int(datetime.datetime.now().strftime("%Y%m%d%H%M%S"))

  def restart(self):
    self.id = int(datetime.datetime.now().strftime("%Y%m%d%H%M%S"))

  def write(self, score : int, lines : int, level : int, preview : int, tetromino_in_play : int, spawned : bool, playfield):
    """
    Expects a numpy array as playfield
    """
    time = datetime.datetime.now()
    self._write(score, lines, level, time.strftime("%Y/%m/%d %H:%M:%S.%f"), preview, tetromino_in_play, spawned, playfield.tolist())

  def _write(self, score : int, lines : int, level : int, time : datetime.datetime, preview : int, tetromino_in_play : int, spawned : bool, playfield):
    command = "INSERT INTO rounds (round_id, time, score, lines, level, preview, tetromino_in_play, spawned, playfield) VALUES (" + self._create_sqlite_string(score, lines, level, time, preview, tetromino_in_play, spawned, playfield) + ");"
    #print(command)
    self.con.execute(command)
    self.con.commit()

  def _create_sqlite_string(self, score, lines, level, time, preview, tetromino_in_play, spawned, playfield):
    if(tetromino_in_play is None):
      tetromino_in_play = -99

    return str(self.id) + "," + \
            "\'" + time + "\'," + \
            str(score) + "," + \
            str(lines) + "," + \
            str(level) + "," + \
            str(preview) + "," + \
            str(tetromino_in_play) + "," + \
            str(spawned) + "," + \
            "\'" + json.dumps(playfield) + "\'"