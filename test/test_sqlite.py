import datetime
import os
import time
import unittest

import numpy as np

from tetristracker.commasv.sqlite_reader import SqliteReader
from tetristracker.commasv.sqlite_writer import SqliteWriter


class TestSqlite(unittest.TestCase):
  path = ".temp/"
  file_name = "test.db"
  @classmethod
  def tearDownClass(cls):
    os.rmdir(".temp")

  @classmethod
  def setUpClass(cls):
    os.mkdir(".temp")

  @classmethod
  def tearDown(cls):
    os.remove(cls.path + cls.file_name)

  def test_database_read_and_write_one(self):
    sqlite = SqliteWriter(path=self.path, file_name=self.file_name)
    sqlite.write(1, 2, 3, 4, np.array([[1,2,3,4,5],[6,7,8,9,10]]))
    sqlite_read = SqliteReader(prefix=str(sqlite.id), path=self.path, file_name=self.file_name)
    result = sqlite_read.get_all()[0]
    self.assertTrue(result[1]) # round_id int
    self.assertTrue(result[2]) # timestamp string
    self.assertEqual(1, result[3])
    self.assertEqual(2, result[4])
    self.assertEqual(3, result[5])
    self.assertEqual(4, result[6])
    self.assertSequenceEqual([[1,2,3,4,5],[6,7,8,9,10]], result[7])

  def test_database_read_and_write_multiple_times(self):
    # first "round"
    sqlite = SqliteWriter(path=self.path, file_name=self.file_name)
    sqlite.write(1, 2, 3, 4, np.array([[1,2,3,4,5],[6,7,8,9,10]]))
    sqlite.write(2, 3, 4, 5, np.array([[1, 2, 5, 4, 5], [6, 7, 8, 9, 10]]))

    time.sleep(1)

    # start another "round"
    sqlite = SqliteWriter(path=self.path, file_name=self.file_name)
    sqlite.write(1, 2, 3, 4, np.array([[1, 2, 3, 4, 5], [6, 7, 8, 9, 10]]))
    sqlite.write(2, 3, 4, 5, np.array([[1, 2, 5, 4, 5], [6, 7, 8, 9, 10]]))

    sqlite_read = SqliteReader(prefix=str(sqlite.id), path=self.path, file_name=self.file_name)
    values = sqlite_read.get_all()
    self.assertEqual(2, len(values))

    result = values[0]
    self.assertTrue(result[1]) # round_id int
    self.assertTrue(result[2]) # timestamp string
    self.assertEqual(1, result[3])
    self.assertEqual(2, result[4])
    self.assertEqual(3, result[5])
    self.assertEqual(4, result[6])
    self.assertSequenceEqual([[1,2,3,4,5],[6,7,8,9,10]], result[7])

    result = values[1]
    self.assertTrue(result[1]) # round_id int
    self.assertTrue(result[2]) # timestamp string
    self.assertEqual(2, result[3])
    self.assertEqual(3, result[4])
    self.assertEqual(4, result[5])
    self.assertEqual(5, result[6])
    self.assertSequenceEqual([[1,2,5,4,5],[6,7,8,9,10]], result[7])

  def _write_two_rounds_into_temp_database(self):
    # first "round"
    sqlite = SqliteWriter(path=self.path, file_name=self.file_name)
    sqlite.write(1, 2, 3, 4, np.array([[1,2,3,4,5],[6,7,8,9,10]]))
    sqlite.write(2, 3, 4, 5, np.array([[1, 2, 5, 4, 5], [6, 7, 8, 9, 10]]))

    time.sleep(1)

    # start another "round"
    sqlite = SqliteWriter(path=self.path, file_name=self.file_name)
    sqlite.write(1, 2, 3, 4, np.array([[1, 2, 3, 4, 5], [6, 7, 8, 9, 10]]))
    sqlite.write(2, 3, 4, 5, np.array([[1, 2, 5, 4, 5], [6, 7, 8, 9, 10]]))

  def test_database_round_id_retrieval(self):
    self._write_two_rounds_into_temp_database()

    sqlite_read = SqliteReader(path=self.path, file_name=self.file_name)
    result = sqlite_read.get_round_ids()
    self.assertEqual(2, len(result))

  def test_database_round_retrieval_by_id(self):
    self._write_two_rounds_into_temp_database()

    sqlite_read = SqliteReader(path=self.path, file_name=self.file_name)
    ids = sqlite_read.get_round_ids()
    round_id = ids[0][0]
    result = sqlite_read.get_round(str(round_id))
    self.assertEqual(2, len(result))

  def test_database_round_values_retrieval(self):
    """
    This test only checks whether it returns
    the right classe but not if the values
    are correct (because this would require
    some more sophisticated ways to test it because
    the time is generated within SqliteReader
    class.)
    """
    sqlite = SqliteWriter(path=self.path, file_name=self.file_name)
    sqlite.write(1, 2, 3, 4, np.array([[1,2,3,4,5],[6,7,8,9,10]]))
    sqlite.write(2, 3, 4, 5, np.array([[1, 2, 5, 4, 5], [6, 7, 8, 9, 10]]))

    sqlite_read = SqliteReader(prefix=str(sqlite.id), path=self.path, file_name=self.file_name)
    result = sqlite_read.get_start_and_end_times_per_round()
    self.assertEqual(1, len(result))
    self.assertTrue(isinstance(result[0].start, datetime.datetime))
    self.assertTrue(isinstance(result[0].end, datetime.datetime))
    self.assertTrue(isinstance(result[0].time_passed, datetime.timedelta))





