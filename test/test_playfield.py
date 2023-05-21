import unittest

import numpy as np

from test.helpers import create_gameboy_view_processor_with, create_testing_array_s2, create_testing_array_high_parity, \
  create_testing_array_full_line_grey, create_testing_array_full_line, create_testing_array_s2_next_piece, \
  create_testing_array_s2_without_dropping_piece, get_preview
from tetristracker.processor.playfield_processor import Playfield, PlayfieldProcessor
from tetristracker.tile.tile_recognizer import TileRecognizer
from tetristracker.tracker.playfield_tracker import PlayfieldTracker
from tetristracker.tracker.preview_tracker import PreviewTracker


class TestPlayfield(unittest.TestCase):
  def get_playfield(self, processor):
    playfield_image = processor.get_playfield()
    return PlayfieldProcessor(playfield_image, image_is_tiled=True).run(return_on_transition=True)

  def test_playfield_intersection(self):
    gv1 = create_gameboy_view_processor_with("test/sequence/sequence-1-2.png")
    gv2 = create_gameboy_view_processor_with("test/sequence/sequence-1-3.png")
    playfield_before = self.get_playfield(gv1)
    playfield_after = self.get_playfield(gv2)
    res = playfield_before.intersection(playfield_after)
    self.assertEqual(4,np.sum(res==5))
    self.assertSequenceEqual([5,-99,5,5,-99,5], (res[15:19, 8:10]).flatten().tolist())

    # both direction should yield same result
    res = playfield_after.intersection(playfield_before)
    self.assertEqual(4,np.sum(res==5))
    self.assertSequenceEqual([5,-99,5,5,-99,5], (res[15:19, 8:10]).flatten().tolist())

  def test_same_tetromino_playfield(self):
    gv1 = create_gameboy_view_processor_with("test/sequence/sequence-2-1.png")
    gv2 = create_gameboy_view_processor_with("test/sequence/sequence-2-2.png")
    gv3 = create_gameboy_view_processor_with("test/sequence/sequence-2-3.png")
    gv4 = create_gameboy_view_processor_with("test/sequence/sequence-2-4.png")

    field_tracker = PlayfieldTracker()
    preview_tracker = PreviewTracker()
    field_sequence_1 = self.get_playfield(gv1)
    preview_sequence_1 = get_preview(gv1)
    self.assertEqual(preview_sequence_1, TileRecognizer.T_MINO)
    field_tracker.track(field_sequence_1)
    preview_tracker.track(preview_sequence_1, field_tracker)

    field_tracker = PlayfieldTracker()
    preview_tracker = PreviewTracker()
    field_sequence_2 = self.get_playfield(gv2)
    preview_sequence_2 = get_preview(gv2)
    self.assertEqual(preview_sequence_2, TileRecognizer.T_MINO)
    field_tracker.track(field_sequence_2)
    preview_tracker.track(preview_sequence_2, field_tracker)

    field_tracker = PlayfieldTracker()
    preview_tracker = PreviewTracker()
    field_sequence_3 = self.get_playfield(gv3)
    preview_sequence_3 = get_preview(gv3)
    self.assertEqual(preview_sequence_3, TileRecognizer.S_MINO)
    field_tracker.track(field_sequence_3)
    preview_tracker.track(preview_sequence_3, field_tracker)

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
    playfield_unrelated = self.get_playfield(gv1)
    tracker.track(playfield_unrelated)
    self.assertIsNone(tracker.clean_playfield())

    playfield_before = self.get_playfield(gv2)
    tracker.track(playfield_before)
    self.assertIsNone(tracker.clean_playfield())

    playfield_after = self.get_playfield(gv3)
    tracker.track(playfield_after)
    clean_board = tracker.clean_playfield()
    self.assertEqual(4,np.sum(clean_board==5))
    self.assertSequenceEqual([5,-99,5,5,-99,5], (clean_board[15:19, 8:10]).flatten().tolist())


  def test_playfield_dont_replace_full_row(self):
    playfield = Playfield(create_testing_array_full_line())

    #preconditions
    self.assertSequenceEqual(playfield.playfield_array[11].tolist(), [   3 ,   3 ,   3 ,   9 ,  10,  10,  11,   3,   3,   3 ])
    self.assertEqual(0, playfield.line_clear_count)

    playfield.full_row_replacement()
    self.assertSequenceEqual(playfield.playfield_array[11].tolist(), [3, 3, 3, 9, 10, 10, 11, 3, 3, 3])
    self.assertEqual(0, playfield.line_clear_count)

  def test_playfield_dont_replace_full_grey_row(self):
    playfield = Playfield(create_testing_array_full_line_grey())

    #preconditions
    self.assertSequenceEqual(playfield.playfield_array[11].tolist(), [   12 ,   12 ,   12 ,   12 ,  12,  12,  12,   12,   12,   12 ])
    self.assertEqual(0, playfield.line_clear_count)

    playfield.full_row_replacement()
    self.assertSequenceEqual(playfield.playfield_array[11].tolist(), [ -99 , -99 , -99 , -99 , -99, -99, -99, -99, -99, -99 ])
    self.assertEqual(1, playfield.line_clear_count)

  def test_playfield_count_minos(self):
    playfield = Playfield(create_testing_array_full_line_grey())
    self.assertEqual(44, playfield.count_minos())
    playfield.full_row_replacement()
    self.assertEqual(44, playfield.count_minos())
    self.assertEqual(34, playfield.count_minos(without_cleared_lines=True))

  def test_playfield_empty(self):
    empty = Playfield.empty()
    self.assertEqual(10, empty.playfield_array.shape[1])
    self.assertEqual(18, empty.playfield_array.shape[0])
    self.assertTrue(np.sum(empty.playfield_array[empty.playfield_array != -99]) == 0)

  def test_playfield_checkerboard_mask(self):
    checker = Playfield.checkerboard_mask()
    self.assertEqual(10, checker.shape[1])
    self.assertEqual(18, checker.shape[0])
    checker2 = Playfield.checkerboard_mask(start=0)
    self.assertTrue(np.sum(checker & checker2) == 0)
    self.assertTrue(np.sum(checker | checker2) == 180)

  def test_surface_trace(self):
    playfield2 = Playfield(create_testing_array_high_parity())
    trace = playfield2.surface_trace()
    self.assertSequenceEqual(trace.tolist(), [0,0,1,1,-1,-1,1,1,-1])

  def test_surface_trace_2(self):
    playfield2 = Playfield(create_testing_array_s2_without_dropping_piece())
    trace = playfield2.surface_trace()
    self.assertSequenceEqual(trace.tolist(), [13, 0, -1, 3, 0, -3, 2, 0, 1])

  def test_possibilities_2(self):
    playfield2 = Playfield(create_testing_array_s2_without_dropping_piece())
    res = playfield2.possibilities()
    self.assertSequenceEqual(res.tolist(), [ 3,  4,  5,  7,  8, 11, 14, 15, 19, 21, 22])

  def test_possibilities_3(self):
    playfield = Playfield.empty()
    res = playfield.possibilities()
    # on an empty board S (14) and Z (10) are not ideal
    self.assertSequenceEqual(res.tolist(), [2, 3, 5, 6, 8, 20, 22])

  def test_parity(self):
    playfield = Playfield(create_testing_array_s2())
    self.assertEqual(0, playfield.parity())

    playfield2 = Playfield(create_testing_array_high_parity())
    self.assertEqual(4, playfield2.parity())

  def test_playfield_has_empty_line_at(self):
    playfield = Playfield(create_testing_array_full_line_grey())
    playfield.full_row_replacement()
    self.assertFalse(playfield.has_empty_line_at(10))
    self.assertTrue(playfield.has_empty_line_at(11))
    self.assertFalse(playfield.has_empty_line_at(12))

  def test_playfield_equal(self):
    playfield = Playfield(create_testing_array_full_line())
    # Should be equal to itself
    self.assertTrue(playfield.is_equal(playfield))
    playfield2 = Playfield(create_testing_array_s2())
    self.assertFalse(playfield.is_equal(playfield2))

  def test_playfield_all_but(self):
    playfield1 = Playfield(create_testing_array_s2())
    reduced_playfield = playfield1.all_but(TileRecognizer.L_MINO)
    self.assertEqual(8, reduced_playfield.count_minos())

  def test_playfield_mino_difference(self):
    playfield1 = Playfield(create_testing_array_s2())
    playfield2 = Playfield(create_testing_array_s2_next_piece())

    comparison_mino = playfield1.mino_difference(playfield2)
    # There should be four new minos
    self.assertEqual(4, comparison_mino)

    comparison_mino = playfield2.mino_difference(playfield1)
    self.assertEqual(-4, comparison_mino)

  def test_playfield_same_minos_true(self):
    gv1 = create_gameboy_view_processor_with("test/sequence/sequence-1-2.png")
    gv2 = create_gameboy_view_processor_with("test/sequence/sequence-1-3.png")

    playfield1 = self.get_playfield(gv1)
    playfield2 = self.get_playfield(gv2)

    self.assertTrue(playfield1.same_minos(playfield2))

  def test_playfield_same_minos_false(self):
    gv1 = create_gameboy_view_processor_with("test/sequence/sequence-1-1.png")
    gv2 = create_gameboy_view_processor_with("test/sequence/sequence-1-2.png")

    playfield1 = self.get_playfield(gv1)
    playfield2 = self.get_playfield(gv2)

    self.assertFalse(playfield1.same_minos(playfield2))


  def test_playfield_difference(self):
    playfield1 = Playfield(create_testing_array_s2())
    playfield2 = Playfield(create_testing_array_s2_next_piece())

    comparison_mino = playfield1.mino_difference(playfield2)
    # There should be four new minos
    self.assertEqual(4, comparison_mino)

    playfield_difference = playfield2.playfield_difference(playfield1)
    # L-piece is now on the left and previously occupied
    # the space of the s piece. Which leaves a piece of
    # the s-piece visible.
    self.assertEqual(5, playfield_difference.count_minos())

    playfield_difference = playfield1.playfield_difference(playfield2)

    # The s-piece covers the l-piece an only leave one
    # edge of the l-piece

    self.assertEqual(1, playfield_difference.count_minos())

  def test_playfield_line_clear(self):
    processor = create_gameboy_view_processor_with("test/full-view/gameboy-full-view-tetris.png")
    playfield_processor = PlayfieldProcessor(processor.get_playfield(), image_is_tiled=True)
    playfield = playfield_processor.run(save_tiles=True)
    self.assertEqual(1, playfield.line_clear_count)
    self.assertTrue(playfield.is_line_clear())

  def test_playfield_line_clear_2(self):
    processor = create_gameboy_view_processor_with("test/full-view/gameboy-full-view-tetris-2.png")
    playfield_processor = PlayfieldProcessor(processor.get_playfield(), image_is_tiled=True)
    playfield = playfield_processor.run(save_tiles=True)
    self.assertEqual(2, playfield.line_clear_count)
    self.assertTrue(playfield.is_line_clear())

  def test_playfield_non_line_clear(self):
    processor = create_gameboy_view_processor_with("test/full-view/gameboy-full-view-non-tetris.png")
    playfield_processor = PlayfieldProcessor(processor.get_playfield(), image_is_tiled=True)
    playfield = playfield_processor.run()
    self.assertEqual(0, playfield.line_clear_count)
    self.assertFalse(playfield.is_line_clear())