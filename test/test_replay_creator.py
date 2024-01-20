import json
import unittest

from test.helpers import create_testing_array_full_view
from tetristracker.helpers.calculations import number_to_hex_string
from tetristracker.recreator.replay_creator import ReplayCreator
from tetristracker.tile.tetromino_transmission import TetrominoTransmission
from tetristracker.tile.tile_recognizer import TileRecognizer


class TestReplayCreator(unittest.TestCase):
  def test_always_256_pieces(self):
    test_array = [[0,0,0,0,0,0,0,TileRecognizer.S_MINO,True, create_testing_array_full_view()],
                  [0,0,0,0,0,0,0,TileRecognizer.T_MINO,False, create_testing_array_full_view()]]

    replay = ReplayCreator(test_array, 0)
    values = replay.create()
    # Maximum of 256 pieces (two chars per number)
    self.assertEqual(ReplayCreator.MAX_PIECES*2, len(values['pieces']))

  def test_correct_pieces(self):
    test_array = [[0,0,0,0,0,0,0,TileRecognizer.S_MINO,True, create_testing_array_full_view()],
                  [0,0,0,0,0,0,0,TileRecognizer.T_MINO,False, create_testing_array_full_view()]]

    replay = ReplayCreator(test_array, 0)
    values = replay.create()
    self.assertEqual(number_to_hex_string(TetrominoTransmission.S_TETROMINO), values['pieces'][0:2])
    self.assertEqual(number_to_hex_string(TetrominoTransmission.L_TETROMINO), values['pieces'][2:4])

  def test_correct_garbage(self):
    test_array = [[0, 0, 0, 0, 0, 0, 0, TileRecognizer.S_MINO, True, create_testing_array_full_view()],
                  [0, 0, 0, 0, 0, 0, 0, TileRecognizer.T_MINO, False, create_testing_array_full_view()]]

    replay = ReplayCreator(test_array, 0)
    values = replay.create()
    self.assertEqual(200, len(values["garbage"]))
    print(json.dumps(values['garbage']))