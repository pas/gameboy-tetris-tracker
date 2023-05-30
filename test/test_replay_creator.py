import unittest

from tetristracker.recreator.replay_creator import ReplayCreator
from tetristracker.tile.tile_recognizer import TileRecognizer


class TestReplayCreator(unittest.TestCase):
  def test_always_30_pieces(self):
    test_array = [[0,0,0,0,0,0,TileRecognizer.S_MINO,True,[]],
                  [0,0,0,0,0,0,TileRecognizer.T_MINO,False,[]]]

    replay = ReplayCreator(test_array, 0)
    pieces = replay.save("")
    self.assertEqual(30, len(pieces))
    self.assertEqual(TileRecognizer.S_MINO, pieces[0])
