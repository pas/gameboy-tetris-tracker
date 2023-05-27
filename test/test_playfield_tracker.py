import unittest

import numpy as np

from test.helpers import create_gameboy_view_processor_with, get_preview, get_playfield
from tetristracker.tile.tile_recognizer import TileRecognizer
from tetristracker.tracker.playfield_tracker import PlayfieldTracker
from tetristracker.tracker.preview_tracker import PreviewTracker


class TestPlayfieldTracker(unittest.TestCase):
  def test_line_clear_detection(self):
    gv1 = create_gameboy_view_processor_with("test/sequence/sequence-4-1.png")
    gv2 = create_gameboy_view_processor_with("test/sequence/sequence-4-2.png")
    tracker = PlayfieldTracker()
    playfield1 = get_playfield(gv1)
    tracker.track(playfield1)
    playfield2 = get_playfield(gv2)
    tracker.track(playfield2)
    self.assertTrue(tracker.was_line_clear())

  def test_only_active_tetromino_playfield(self):
    gv1 = create_gameboy_view_processor_with("test/sequence/sequence-1-1.png")
    gv2 = create_gameboy_view_processor_with("test/sequence/sequence-1-2.png")
    gv3 = create_gameboy_view_processor_with("test/sequence/sequence-1-3.png")

    tracker = PlayfieldTracker()
    playfield_one_tetromino = self.get_playfield(gv1)
    tracker.track(playfield_one_tetromino)
    board = tracker.only_active_tetromino()
    self.assertEqual(4, np.sum(board.playfield_array == TileRecognizer.S_MINO))
    self.assertSequenceEqual([TileRecognizer.S_MINO, TileRecognizer.EMPTY,
                              TileRecognizer.S_MINO, TileRecognizer.S_MINO,
                              TileRecognizer.EMPTY, TileRecognizer.S_MINO], board.playfield_array[14:17 ,8:10].flatten().tolist())

    # Because in the last frame the active tetromino was
    # not locked it cannot make a clear difference. Therefore
    # this returns none
    playfield_next_tetromino = self.get_playfield(gv2)
    tracker.track(playfield_next_tetromino)
    board = tracker.only_active_tetromino()
    self.assertIsNone(board)

    playfield_next_next_tetromino = self.get_playfield(gv3)
    tracker.track(playfield_next_next_tetromino)
    board = tracker.only_active_tetromino()
    self.assertEqual(4, np.sum(board.playfield_array == TileRecognizer.Z_MINO))
    self.assertSequenceEqual([TileRecognizer.Z_MINO, TileRecognizer.Z_MINO, TileRecognizer.EMPTY,
                              TileRecognizer.EMPTY, TileRecognizer.Z_MINO, TileRecognizer.Z_MINO], board.playfield_array[1:3 ,3:6].flatten().tolist())

  def test_clean_playfield(self):
    gv1 = create_gameboy_view_processor_with("test/sequence/sequence-1-1.png")
    gv2 = create_gameboy_view_processor_with("test/sequence/sequence-1-2.png")
    gv3 = create_gameboy_view_processor_with("test/sequence/sequence-1-3.png")

    tracker = PlayfieldTracker()
    playfield_unrelated = get_playfield(gv1)
    tracker.track(playfield_unrelated)
    self.assertIsNone(tracker.clean_playfield())

    playfield_before = get_playfield(gv2)
    tracker.track(playfield_before)
    self.assertIsNone(tracker.clean_playfield())

    playfield_after = get_playfield(gv3)
    tracker.track(playfield_after)
    clean_board = tracker.clean_playfield()
    self.assertEqual(4,np.sum(clean_board==5))
    self.assertSequenceEqual([5,-99,5,5,-99,5], (clean_board[15:19, 8:10]).flatten().tolist())

  def test_clean_playfield_(self):
    gv1 = create_gameboy_view_processor_with("test/sequence/sequence-2-1.png")
    gv2 = create_gameboy_view_processor_with("test/sequence/sequence-2-2.png")

    tracker = PlayfieldTracker()

    playfield_before = get_playfield(gv1)
    tracker.track(playfield_before)
    self.assertIsNone(tracker.clean_playfield())

    playfield_after = get_playfield(gv2)
    tracker.track(playfield_after)
    clean_board = tracker.clean_playfield()
    # 16x10 = 160 + 8 in the last two lines
    self.assertEqual(168,np.sum(clean_board==-99))
    self.assertSequenceEqual([-99,   0, -99, -99, -99, -99,   5,   5,   4, -99,
                              -99,   0,   0,   0, -99,   5,   5,   4,   4,   4], (clean_board[16:19, :]).flatten().tolist())

  def test_playfield_tracker_piece_spawning_detection_1(self):
    gv1 = create_gameboy_view_processor_with("test/sequence/sequence-2-1.png")
    gv2 = create_gameboy_view_processor_with("test/sequence/sequence-2-2.png")
    gv3 = create_gameboy_view_processor_with("test/sequence/sequence-2-3.png")
    gv4 = create_gameboy_view_processor_with("test/sequence/sequence-2-4.png")

    field_tracker = PlayfieldTracker()
    preview_tracker = PreviewTracker()
    field_sequence_1 = get_playfield(gv1)
    preview_sequence_1 = get_preview(gv1)
    self.assertEqual(preview_sequence_1, TileRecognizer.T_MINO)
    field_tracker.track(field_sequence_1)
    preview_tracker.track(preview_sequence_1, field_tracker)
    self.assertSequenceEqual([0,0,0,0,0,0,0], preview_tracker.stats)

    field_sequence_2 = get_playfield(gv2)
    preview_sequence_2 = get_preview(gv2)
    self.assertEqual(preview_sequence_2, TileRecognizer.T_MINO)
    field_tracker.track(field_sequence_2)
    preview_tracker.track(preview_sequence_2, field_tracker)
    self.assertSequenceEqual([0, 0, 0, 0, 0, 0, 0], preview_tracker.stats)

    field_sequence_3 = get_playfield(gv3)
    preview_sequence_3 = get_preview(gv3)
    self.assertEqual(preview_sequence_3, TileRecognizer.S_MINO)
    field_tracker.track(field_sequence_3)
    preview_tracker.track(preview_sequence_3, field_tracker)
    print(preview_tracker.stats)
    self.assertSequenceEqual([0, 0, 0, 0, 0, 0, 0], preview_tracker.stats)

    field_sequence_4 = get_playfield(gv4)
    preview_sequence_4 = get_preview(gv4)
    self.assertEqual(preview_sequence_4, TileRecognizer.S_MINO)
    field_tracker.track(field_sequence_4)
    preview_tracker.track(preview_sequence_4, field_tracker)
    self.assertSequenceEqual([0, 0, 0, 0, 1, 0, 0], preview_tracker.stats)

  def test_playfield_tracker_piece_spawning_detection_2(self):
    gv1 = create_gameboy_view_processor_with("test/sequence/sequence-1-1.png")
    gv2 = create_gameboy_view_processor_with("test/sequence/sequence-1-2.png")
    gv3 = create_gameboy_view_processor_with("test/sequence/sequence-1-3.png")

    field_tracker = PlayfieldTracker()
    preview_tracker = PreviewTracker()
    field_sequence_1 = get_playfield(gv1)
    preview_sequence_1 = get_preview(gv1)
    self.assertEqual(preview_sequence_1, TileRecognizer.Z_MINO)
    field_tracker.track(field_sequence_1)
    preview_tracker.track(preview_sequence_1, field_tracker)
    self.assertSequenceEqual([0,0,0,0,0,0,0], preview_tracker.stats)

    field_sequence_2 = get_playfield(gv2)
    preview_sequence_2 = get_preview(gv2)
    self.assertEqual(preview_sequence_2, TileRecognizer.O_MINO)
    field_tracker.track(field_sequence_2)
    preview_tracker.track(preview_sequence_2, field_tracker)
    self.assertSequenceEqual([0, 0, 0, 0, 0, 0, 0], preview_tracker.stats)

    field_sequence_3 = get_playfield(gv3)
    preview_sequence_3 = get_preview(gv3)
    self.assertEqual(preview_sequence_3, TileRecognizer.O_MINO)
    field_tracker.track(field_sequence_3)
    preview_tracker.track(preview_sequence_3, field_tracker)
    print(preview_tracker.stats)
    self.assertSequenceEqual([0, 0, 0, 0, 0, 0, 0], preview_tracker.stats)

  def get_sequence(self, path, until):
    gvs = []
    for number in range(until):
      gvs.append(create_gameboy_view_processor_with(path + "-" + str(number+1) + ".png"))
    return gvs

  def prepare_playfield_and_preview(self, gv,  field_tracker, preview_tracker):
    field_sequence_1 = get_playfield(gv)
    preview_sequence_1 = get_preview(gv)
    field_tracker.track(field_sequence_1)
    preview_tracker.track(preview_sequence_1, field_tracker)

  def test_playfield_tracker_piece_spawning_detection_3(self):
    gvs = self.get_sequence("test/sequence/sequence-3", 10)

    expected = [
      [0, 0, 0, 0, 0, 0, 0], # 3-1
      [0, 0, 0, 0, 0, 0, 0], # 3-2
      [0, 0, 0, 0, 0, 0, 0], # 3-3
      [0, 0, 0, 0, 0, 0, 0], # 3-4 s-mino spawned
      [0, 0, 0, 0, 0, 1, 0], # 3-5 s-mino counted
      [0, 0, 0, 0, 0, 1, 0], # 3-6
      [0, 0, 0, 0, 0, 1, 0], # 3-7 o-mino spawned
      [0, 0, 1, 0, 0, 1, 0], # 3-8 o-mino counted
      [0, 0, 1, 0, 0, 1, 0], # 3-9 l-mino spawned
      [1, 0, 1, 0, 0, 1, 0]  # 3-10
    ]

    field_tracker = PlayfieldTracker()
    preview_tracker = PreviewTracker()
    for number, gv in enumerate(gvs):
      self.prepare_playfield_and_preview(gv, field_tracker, preview_tracker)
      self.assertSequenceEqual(expected[number], preview_tracker.stats, "in sequence 3-"+str(number+1))


  def test_playfield_tracker_piece_spawning_detection_full_game(self):
    # 1: expected stats 2: preview of image 3: last preview change
    expected = [
      [[0, 0, 0, 0, 0, 0, 0], TileRecognizer.Z_MINO, TileRecognizer.J_MINO],  # 1
      [[0, 0, 0, 0, 0, 0, 0], TileRecognizer.Z_MINO, TileRecognizer.J_MINO],  # 2
      [[0, 0, 0, 0, 0, 0, 0], TileRecognizer.Z_MINO, TileRecognizer.J_MINO],  # 3
      [[0, 0, 0, 0, 0, 0, 0], TileRecognizer.Z_MINO, TileRecognizer.J_MINO],  # 4
      [[0, 0, 0, 0, 0, 0, 0], TileRecognizer.Z_MINO, TileRecognizer.J_MINO],  # 5
      [[0, 0, 0, 0, 0, 0, 0], TileRecognizer.Z_MINO, TileRecognizer.J_MINO],  # 6
      [[0, 0, 0, 0, 0, 0, 0], TileRecognizer.Z_MINO, TileRecognizer.J_MINO],  # 7
      [[0, 0, 0, 0, 0, 0, 0], TileRecognizer.Z_MINO, TileRecognizer.J_MINO],  # 8
      [[0, 0, 0, 0, 0, 0, 0], TileRecognizer.L_MINO, TileRecognizer.Z_MINO],  # 9
      [[0, 0, 0, 0, 0, 0, 0], TileRecognizer.L_MINO, TileRecognizer.Z_MINO],  # 10

      [[0, 0, 0, 0, 0, 0, 0], TileRecognizer.L_MINO, TileRecognizer.Z_MINO],  # 11
      [[0, 1, 0, 0, 0, 0, 0], TileRecognizer.L_MINO, TileRecognizer.EMPTY],  # 12
      [[0, 1, 0, 0, 0, 0, 0], TileRecognizer.L_MINO, TileRecognizer.EMPTY],  # 13
      [[0, 1, 0, 0, 0, 0, 0], TileRecognizer.L_MINO, TileRecognizer.EMPTY],  # 14
      [[0, 1, 0, 0, 0, 0, 0], TileRecognizer.L_MINO, TileRecognizer.EMPTY],  # 15
      [[0, 1, 0, 0, 0, 0, 0], TileRecognizer.O_MINO, TileRecognizer.L_MINO],  # 16
      [[0, 1, 0, 0, 0, 0, 0], TileRecognizer.O_MINO, TileRecognizer.L_MINO],  # 17
      [[0, 1, 0, 1, 0, 0, 0], TileRecognizer.O_MINO, TileRecognizer.EMPTY],  # 18
      [[0, 1, 0, 1, 0, 0, 0], TileRecognizer.O_MINO, TileRecognizer.EMPTY],  # 19
      [[0, 1, 0, 1, 0, 0, 0], TileRecognizer.O_MINO, TileRecognizer.EMPTY],  # 20

      [[0, 1, 0, 1, 0, 0, 0], TileRecognizer.O_MINO, TileRecognizer.EMPTY],   # 21
      [[0, 1, 0, 1, 0, 0, 0], TileRecognizer.O_MINO, TileRecognizer.EMPTY],   # 22
      [[0, 1, 0, 1, 0, 0, 0], TileRecognizer.O_MINO, TileRecognizer.EMPTY],   # 23
      [[0, 1, 0, 1, 0, 0, 0], TileRecognizer.O_MINO, TileRecognizer.EMPTY],   # 24
      [[0, 1, 0, 1, 0, 0, 0], TileRecognizer.O_MINO, TileRecognizer.EMPTY],  # 25
      # Same piece in preview as just spawned
      [[0, 1, 1, 1, 0, 0, 0], TileRecognizer.O_MINO, TileRecognizer.EMPTY],  # 26
      [[0, 1, 1, 1, 0, 0, 0], TileRecognizer.O_MINO, TileRecognizer.EMPTY],  # 27
      [[0, 1, 1, 1, 0, 0, 0], TileRecognizer.O_MINO, TileRecognizer.EMPTY],  # 28
      [[0, 1, 1, 1, 0, 0, 0], TileRecognizer.O_MINO, TileRecognizer.EMPTY],  # 29
      [[0, 1, 1, 1, 0, 0, 0], TileRecognizer.O_MINO, TileRecognizer.EMPTY],  # 30

      [[0, 1, 1, 1, 0, 0, 0], TileRecognizer.O_MINO, TileRecognizer.EMPTY],  # 31
      [[0, 1, 1, 1, 0, 0, 0], TileRecognizer.T_MINO, TileRecognizer.O_MINO],  # 32
      [[0, 1, 2, 1, 0, 0, 0], TileRecognizer.T_MINO, TileRecognizer.EMPTY],  # 33
      [[0, 1, 2, 1, 0, 0, 0], TileRecognizer.T_MINO, TileRecognizer.EMPTY],  # 34
      [[0, 1, 2, 1, 0, 0, 0], TileRecognizer.T_MINO, TileRecognizer.EMPTY],  # 35
      [[0, 1, 2, 1, 0, 0, 0], TileRecognizer.T_MINO, TileRecognizer.EMPTY],  # 36
      [[0, 1, 2, 1, 0, 0, 0], TileRecognizer.T_MINO, TileRecognizer.EMPTY],  # 37
      [[0, 1, 2, 1, 0, 0, 0], TileRecognizer.T_MINO, TileRecognizer.EMPTY],  # 38
      [[0, 1, 2, 1, 0, 0, 0], TileRecognizer.J_MINO, TileRecognizer.T_MINO],  # 39
      [[0, 1, 2, 1, 1, 0, 0], TileRecognizer.J_MINO, TileRecognizer.EMPTY],  # 40

      [[0, 1, 2, 1, 1, 0, 0], TileRecognizer.J_MINO, TileRecognizer.EMPTY],  # 41
      [[0, 1, 2, 1, 1, 0, 0], TileRecognizer.J_MINO, TileRecognizer.EMPTY],  # 42
      [[0, 1, 2, 1, 1, 0, 0], TileRecognizer.J_MINO, TileRecognizer.EMPTY],  # 43
      [[0, 1, 2, 1, 1, 0, 0], TileRecognizer.J_MINO, TileRecognizer.EMPTY],  # 44
      [[0, 1, 2, 1, 1, 0, 0], TileRecognizer.J_MINO, TileRecognizer.EMPTY],  # 45
      [[0, 1, 2, 1, 1, 0, 0], TileRecognizer.J_MINO, TileRecognizer.EMPTY],  # 46
      [[0, 1, 2, 1, 1, 0, 0], TileRecognizer.J_MINO, TileRecognizer.EMPTY],  # 47
      # Same piece in preview as just spawned
      [[1, 1, 2, 1, 1, 0, 0], TileRecognizer.J_MINO, TileRecognizer.EMPTY],  # 48
      [[1, 1, 2, 1, 1, 0, 0], TileRecognizer.J_MINO, TileRecognizer.EMPTY],  # 49
      [[1, 1, 2, 1, 1, 0, 0], TileRecognizer.J_MINO, TileRecognizer.EMPTY],  # 50

      [[1, 1, 2, 1, 1, 0, 0], TileRecognizer.O_MINO, TileRecognizer.J_MINO],  # 51
      [[2, 1, 2, 1, 1, 0, 0], TileRecognizer.O_MINO, TileRecognizer.EMPTY],  # 52
      [[2, 1, 2, 1, 1, 0, 0], TileRecognizer.O_MINO, TileRecognizer.EMPTY],  # 53
      [[2, 1, 2, 1, 1, 0, 0], TileRecognizer.O_MINO, TileRecognizer.EMPTY],  # 54
      [[2, 1, 2, 1, 1, 0, 0], TileRecognizer.O_MINO, TileRecognizer.EMPTY],  # 55
      [[2, 1, 2, 1, 1, 0, 0], TileRecognizer.O_MINO, TileRecognizer.EMPTY],  # 56
      [[2, 1, 2, 1, 1, 0, 0], TileRecognizer.O_MINO, TileRecognizer.EMPTY],  # 57
      [[2, 1, 2, 1, 1, 0, 0], TileRecognizer.O_MINO, TileRecognizer.EMPTY],  # 58
      [[2, 1, 2, 1, 1, 0, 0], TileRecognizer.Z_MINO, TileRecognizer.O_MINO],  # 59
      [[2, 1, 3, 1, 1, 0, 0], TileRecognizer.Z_MINO, TileRecognizer.EMPTY],  # 60

      [[2, 1, 3, 1, 1, 0, 0], TileRecognizer.Z_MINO, TileRecognizer.EMPTY],  # 61
      [[2, 1, 3, 1, 1, 0, 0], TileRecognizer.Z_MINO, TileRecognizer.EMPTY],  # 62
      [[2, 1, 3, 1, 1, 0, 0], TileRecognizer.Z_MINO, TileRecognizer.EMPTY],  # 63
      [[2, 1, 3, 1, 1, 0, 0], TileRecognizer.Z_MINO, TileRecognizer.EMPTY],  # 64
      [[2, 1, 3, 1, 1, 0, 0], TileRecognizer.T_MINO, TileRecognizer.Z_MINO],  # 65
      [[2, 1, 3, 1, 1, 0, 0], TileRecognizer.T_MINO, TileRecognizer.Z_MINO],  # 66
      [[2, 2, 3, 1, 1, 0, 0], TileRecognizer.T_MINO, TileRecognizer.EMPTY],  # 67
      [[2, 2, 3, 1, 1, 0, 0], TileRecognizer.T_MINO, TileRecognizer.EMPTY],  # 68
      [[2, 2, 3, 1, 1, 0, 0], TileRecognizer.T_MINO, TileRecognizer.EMPTY],  # 69
      [[2, 2, 3, 1, 1, 0, 0], TileRecognizer.T_MINO, TileRecognizer.EMPTY],  # 70

      [[2, 2, 3, 1, 1, 0, 0], TileRecognizer.O_MINO, TileRecognizer.T_MINO],  # 71
      [[2, 2, 3, 1, 2, 0, 0], TileRecognizer.O_MINO, TileRecognizer.EMPTY],  # 72
      [[2, 2, 3, 1, 2, 0, 0], TileRecognizer.O_MINO, TileRecognizer.EMPTY],  # 73
      [[2, 2, 3, 1, 2, 0, 0], TileRecognizer.O_MINO, TileRecognizer.EMPTY],  # 74
      [[2, 2, 3, 1, 2, 0, 0], TileRecognizer.O_MINO, TileRecognizer.EMPTY],  # 75
      [[2, 2, 3, 1, 2, 0, 0], TileRecognizer.O_MINO, TileRecognizer.EMPTY],  # 76
      [[2, 2, 3, 1, 2, 0, 0], TileRecognizer.I_MINO_SIMPLE, TileRecognizer.O_MINO],  # 77
      [[2, 2, 4, 1, 2, 0, 0], TileRecognizer.I_MINO_SIMPLE, TileRecognizer.EMPTY],  # 78
      [[2, 2, 4, 1, 2, 0, 0], TileRecognizer.I_MINO_SIMPLE, TileRecognizer.EMPTY],  # 79
      [[2, 2, 4, 1, 2, 0, 0], TileRecognizer.I_MINO_SIMPLE, TileRecognizer.EMPTY],  # 80

      [[2, 2, 4, 1, 2, 0, 0], TileRecognizer.I_MINO_SIMPLE, TileRecognizer.EMPTY],  # 81
      [[2, 2, 4, 1, 2, 0, 0], TileRecognizer.Z_MINO, TileRecognizer.I_MINO_SIMPLE],  # 82
      [[2, 2, 4, 1, 2, 0, 1], TileRecognizer.Z_MINO, TileRecognizer.EMPTY],  # 83
      [[2, 2, 4, 1, 2, 0, 1], TileRecognizer.Z_MINO, TileRecognizer.EMPTY],  # 84
      [[2, 2, 4, 1, 2, 0, 1], TileRecognizer.Z_MINO, TileRecognizer.EMPTY],  # 85
      [[2, 2, 4, 1, 2, 0, 1], TileRecognizer.Z_MINO, TileRecognizer.EMPTY],  # 86
      [[2, 2, 4, 1, 2, 0, 1], TileRecognizer.Z_MINO, TileRecognizer.EMPTY],  # 87
      [[2, 2, 4, 1, 2, 0, 1], TileRecognizer.Z_MINO, TileRecognizer.EMPTY],  # 88
      [[2, 2, 4, 1, 2, 0, 1], TileRecognizer.Z_MINO, TileRecognizer.EMPTY],  # 89

      [[2, 2, 4, 1, 2, 0, 1], TileRecognizer.Z_MINO, TileRecognizer.EMPTY],  # 90
      [[2, 2, 4, 1, 2, 0, 1], TileRecognizer.Z_MINO, TileRecognizer.EMPTY],  # 91
      [[2, 2, 4, 1, 2, 0, 1], TileRecognizer.S_MINO, TileRecognizer.Z_MINO],  # 92
      [[2, 3, 4, 1, 2, 0, 1], TileRecognizer.S_MINO, TileRecognizer.EMPTY],  # 93
      [[2, 3, 4, 1, 2, 0, 1], TileRecognizer.S_MINO, TileRecognizer.EMPTY],  # 94
      [[2, 3, 4, 1, 2, 0, 1], TileRecognizer.S_MINO, TileRecognizer.EMPTY],  # 95
      [[2, 3, 4, 1, 2, 0, 1], TileRecognizer.S_MINO, TileRecognizer.EMPTY],  # 96
      [[2, 3, 4, 1, 2, 0, 1], TileRecognizer.S_MINO, TileRecognizer.EMPTY],  # 97
      [[2, 3, 4, 1, 2, 0, 1], TileRecognizer.S_MINO, TileRecognizer.EMPTY],  # 98
      [[2, 3, 4, 1, 2, 1, 1], TileRecognizer.S_MINO, TileRecognizer.EMPTY],  # 99
      [[2, 3, 4, 1, 2, 1, 1], TileRecognizer.S_MINO, TileRecognizer.EMPTY],  # 100

      [[2, 3, 4, 1, 2, 1, 1], TileRecognizer.S_MINO, TileRecognizer.EMPTY],  # 101
      [[2, 3, 4, 1, 2, 1, 1], TileRecognizer.T_MINO, TileRecognizer.S_MINO],  # 102
      [[2, 3, 4, 1, 2, 2, 1], TileRecognizer.T_MINO, TileRecognizer.EMPTY],  # 103
      [[2, 3, 4, 1, 2, 2, 1], TileRecognizer.T_MINO, TileRecognizer.EMPTY],  # 104
      [[2, 3, 4, 1, 2, 2, 1], TileRecognizer.T_MINO, TileRecognizer.EMPTY],  # 105
      [[2, 3, 4, 1, 2, 2, 1], TileRecognizer.J_MINO, TileRecognizer.T_MINO],  # 106
      [[2, 3, 4, 1, 3, 2, 1], TileRecognizer.J_MINO, TileRecognizer.EMPTY],  # 107
      [[2, 3, 4, 1, 3, 2, 1], TileRecognizer.J_MINO, TileRecognizer.EMPTY],  # 108
      [[2, 3, 4, 1, 3, 2, 1], TileRecognizer.J_MINO, TileRecognizer.EMPTY],  # 109
      [[2, 3, 4, 1, 3, 2, 1], TileRecognizer.S_MINO, TileRecognizer.J_MINO],  # 110
    ]

    gvs = self.get_sequence("test/sequence/full-game/running", len(expected))

    field_tracker = PlayfieldTracker()
    preview_tracker = PreviewTracker()
    preview_tracker.track(TileRecognizer.J_MINO, field_tracker)
    for number, gv in enumerate(gvs):
      #print("running-" + str(number+1))
      self.prepare_playfield_and_preview(gv, field_tracker, preview_tracker)
      self.assertSequenceEqual(preview_tracker.stats, expected[number][0], "in running-"+str(number+1))
      self.assertEqual(expected[number][1], preview_tracker.last(), "for current preview in running-"+str(number+1))
      self.assertEqual(expected[number][2], preview_tracker.remember_preview, "for last preview in running-" + str(number + 1))