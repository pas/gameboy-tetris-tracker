import unittest

from test.helpers import create_testing_array_s2
from tetristracker.image.playfield_recreator import PlayfieldRecreator


class TestCSV(unittest.TestCase):
  def test_playfield_recreator(self):
    recreator = PlayfieldRecreator()
    playfield = create_testing_array_s2()
    recreator.recreate(playfield, 'test/screenshot-playfield-recreation.png')