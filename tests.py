import unittest

from game import Round, Game
from playfield_processor import PlayfieldProcessor, Playfield
from plotter import Plotter
from preview_processor import PreviewProcessor
from gameboy_view_processor import GameboyViewProcessor
from number_processor import NumberProcessor, SequentialNumberProcessor
from playfield_recreator import PlayfieldRecreator
from gameboy_image import GameboyImage
from PIL import Image
import numpy as np

from score_tracker import PreviewTracker, PlayfieldTracker
from stats_image import StatsImage
from tile_recognizer import TileRecognizer, Tile, Tiler, Tetromino
from runner import Runner
from csvfile import CSVReader
import cv2
from capturer import OCVCapturer, MSSCapturer, Capturer
import yaml
from image_manipulator import convert_to_4bitgrey

class MockCSVWriter():
    def __init__(self):
        self.calls = 0

    def write(self, accepted_score, accepted_lines, current_preview, current_playfield):
        self.calls += 1


class StaticCapturer(Capturer):
  def __init__(self, image_path):
    self.static_image = np.array(Image.open(image_path).convert('RGB'))

  def grab_image(self):
    return self.static_image


class TestPlayfieldProcessor(unittest.TestCase):
  def test_cv_capturer(self):
    capturer = OCVCapturer()

  def test_image_manipulator(self):
    image = np.array(Image.open("test/gameboy-full-view.png").convert('RGB'))
    image = convert_to_4bitgrey(image)
    print(image)
    cv2.imwrite("screenshots/reduced_grey_scale.png", image)

  def test_mss_capturer(self):
    with open('config.yml', 'r') as config_file:
      configs = yaml.safe_load(config_file)
      bounding_box = configs["bounding_box"]

    capturer = MSSCapturer(bounding_box)
    image = capturer.grab_image()
    cv2.imwrite("screenshots/non-trimmed.png", image)
    image = capturer.trim(image)
    cv2.imwrite("screenshots/trimmed.png", image)

  def test_playfield_intersection(self):
    gv1 = self.create_gameboy_view_processor_with("test/sequence/sequence-1-2.png")
    gv2 = self.create_gameboy_view_processor_with("test/sequence/sequence-1-3.png")
    runner = Runner()
    playfield_before = self.get_playfield_processor(gv1)
    playfield_after = self.get_playfield_processor(gv2)
    res = playfield_before.intersection(playfield_after)
    self.assertEqual(4,np.sum(res==5))
    self.assertSequenceEqual([5,-99,5,5,-99,5], (res[15:19, 8:10]).flatten().tolist())

    # both direction should yield same result
    res = playfield_after.intersection(playfield_before)
    self.assertEqual(4,np.sum(res==5))
    self.assertSequenceEqual([5,-99,5,5,-99,5], (res[15:19, 8:10]).flatten().tolist())

  def get_playfield_processor(self, processor):
    playfield_image = processor.get_playfield()
    return PlayfieldProcessor(playfield_image, image_is_tiled=True).run(return_on_transition=True)

  def test_same_tetromino_playfield(self):
    gv1 = self.create_gameboy_view_processor_with("test/sequence/sequence-2-1.png")
    gv2 = self.create_gameboy_view_processor_with("test/sequence/sequence-2-2.png")
    gv3 = self.create_gameboy_view_processor_with("test/sequence/sequence-2-3.png")
    gv4 = self.create_gameboy_view_processor_with("test/sequence/sequence-2-4.png")

    tracker = PlayfieldTracker()
    sequence_1 = self.get_playfield_processor(gv1)
    tracker.track(sequence_1)
    distance = tracker.tetromino_distance()
    self.assertIsNone(distance)

    # We need a atleast three images: First one as comparison,
    # second one to find the tetromino and third one to
    # calculate the distance
    sequence_2 = self.get_playfield_processor(gv2)
    tracker.track(sequence_2)
    distance = tracker.tetromino_distance()
    self.assertIsNone(distance)

    sequence_3 = self.get_playfield_processor(gv3)
    tracker.track(sequence_3)
    distance = tracker.tetromino_distance()
    self.assertEqual(distance, -8)

    sequence_4 = self.get_playfield_processor(gv4)
    tracker.track(sequence_4)
    distance = tracker.tetromino_distance()
    self.assertEqual(distance, 4)


  def test_only_active_tetromino_playfield(self):
    gv1 = self.create_gameboy_view_processor_with("test/sequence/sequence-1-1.png")
    gv2 = self.create_gameboy_view_processor_with("test/sequence/sequence-1-2.png")
    gv3 = self.create_gameboy_view_processor_with("test/sequence/sequence-1-3.png")

    tracker = PlayfieldTracker()
    playfield_one_tetromino = self.get_playfield_processor(gv1)
    tracker.track(playfield_one_tetromino)
    board = tracker.only_active_tetromino()
    self.assertEqual(4, np.sum(board.playfield_array == TileRecognizer.S_MINO))
    self.assertSequenceEqual([TileRecognizer.S_MINO, TileRecognizer.EMPTY,
                              TileRecognizer.S_MINO, TileRecognizer.S_MINO,
                              TileRecognizer.EMPTY, TileRecognizer.S_MINO], board.playfield_array[14:17 ,8:10].flatten().tolist())

    # Because in the last frame the active tetromino was
    # not locked it cannot make a clear difference. Therefore
    # this returns none
    playfield_next_tetromino = self.get_playfield_processor(gv2)
    tracker.track(playfield_next_tetromino)
    board = tracker.only_active_tetromino()
    self.assertIsNone(board)

    playfield_next_next_tetromino = self.get_playfield_processor(gv3)
    tracker.track(playfield_next_next_tetromino)
    board = tracker.only_active_tetromino()
    self.assertEqual(4, np.sum(board.playfield_array == TileRecognizer.Z_MINO))
    self.assertSequenceEqual([TileRecognizer.Z_MINO, TileRecognizer.Z_MINO, TileRecognizer.EMPTY,
                              TileRecognizer.EMPTY, TileRecognizer.Z_MINO, TileRecognizer.Z_MINO], board.playfield_array[1:3 ,3:6].flatten().tolist())


  def test_clean_playfield(self):
    gv1 = self.create_gameboy_view_processor_with("test/sequence/sequence-1-1.png")
    gv2 = self.create_gameboy_view_processor_with("test/sequence/sequence-1-2.png")
    gv3 = self.create_gameboy_view_processor_with("test/sequence/sequence-1-3.png")

    tracker = PlayfieldTracker()
    playfield_unrelated = self.get_playfield_processor(gv1)
    tracker.track(playfield_unrelated)
    self.assertIsNone(tracker.clean_playfield())

    playfield_before = self.get_playfield_processor(gv2)
    tracker.track(playfield_before)
    self.assertIsNone(tracker.clean_playfield())

    playfield_after = self.get_playfield_processor(gv3)
    tracker.track(playfield_after)
    clean_board = tracker.clean_playfield()
    self.assertEqual(4,np.sum(clean_board==5))
    self.assertSequenceEqual([5,-99,5,5,-99,5], (clean_board[15:19, 8:10]).flatten().tolist())


  def test_playfield_dont_replace_full_row(self):
    playfield = Playfield(self.create_testing_array_full_line())

    #preconditions
    self.assertSequenceEqual(playfield.playfield_array[11].tolist(), [   3 ,   3 ,   3 ,   9 ,  10,  10,  11,   3,   3,   3 ])
    self.assertEqual(0, playfield.line_clear_count)

    playfield.full_row_replacement()
    self.assertSequenceEqual(playfield.playfield_array[11].tolist(), [3, 3, 3, 9, 10, 10, 11, 3, 3, 3])
    self.assertEqual(0, playfield.line_clear_count)

  def test_playfield_dont_replace_full_grey_row(self):
    playfield = Playfield(self.create_testing_array_full_line_grey())

    #preconditions
    self.assertSequenceEqual(playfield.playfield_array[11].tolist(), [   12 ,   12 ,   12 ,   12 ,  12,  12,  12,   12,   12,   12 ])
    self.assertEqual(0, playfield.line_clear_count)

    playfield.full_row_replacement()
    self.assertSequenceEqual(playfield.playfield_array[11].tolist(), [ -99 , -99 , -99 , -99 , -99, -99, -99, -99, -99, -99 ])
    self.assertEqual(1, playfield.line_clear_count)

  def test_playfield_count_minos(self):
    playfield = Playfield(self.create_testing_array_full_line_grey())
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
    playfield2 = Playfield(self.create_testing_array_high_parity())
    trace = playfield2.surface_trace()
    self.assertSequenceEqual(trace.tolist(), [0,0,1,1,-1,-1,1,1,-1])

  def test_surface_trace_2(self):
    playfield2 = Playfield(self.create_testing_array_s2_without_dropping_piece())
    trace = playfield2.surface_trace()
    self.assertSequenceEqual(trace.tolist(), [13, 0, -1, 3, 0, -3, 2, 0, 1])

  def test_possibilities_2(self):
    playfield2 = Playfield(self.create_testing_array_s2_without_dropping_piece())
    res = playfield2.possibilities()
    self.assertSequenceEqual(res.tolist(), [ 3,  4,  5,  7,  8, 11, 14, 15, 19, 21, 22])

  def test_possibilities_3(self):
    playfield = Playfield.empty()
    res = playfield.possibilities()
    # on an empty board S (14) and Z (10) are not ideal
    self.assertSequenceEqual(res.tolist(), [2, 3, 5, 6, 8, 20, 22])

  def test_parity(self):
    playfield = Playfield(self.create_testing_array_s2())
    self.assertEqual(0, playfield.parity())

    playfield2 = Playfield(self.create_testing_array_high_parity())
    self.assertEqual(4, playfield2.parity())

  def test_playfield_has_empty_line_at(self):
    playfield = Playfield(self.create_testing_array_full_line_grey())
    playfield.full_row_replacement()
    self.assertFalse(playfield.has_empty_line_at(10))
    self.assertTrue(playfield.has_empty_line_at(11))
    self.assertFalse(playfield.has_empty_line_at(12))

  def test_playfield_equal(self):
    playfield = Playfield(self.create_testing_array_full_line())
    # Should be equal to itself
    self.assertTrue(playfield.is_equal(playfield))
    playfield2 = Playfield(self.create_testing_array_s2())
    self.assertFalse(playfield.is_equal(playfield2))

  def test_playfield_all_but(self):
    playfield1 = Playfield(self.create_testing_array_s2())
    reduced_playfield = playfield1.all_but(TileRecognizer.L_MINO)
    self.assertEquals(8, reduced_playfield.count_minos())

  def test_playfield_compare(self):
    playfield1 = Playfield(self.create_testing_array_s2())
    playfield2 = Playfield(self.create_testing_array_s2_next_piece())

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

  def test_gameboy_view_processor_on_pause(self):
      image = np.array(Image.open("test/gameboy-pause-full-view.png").convert('RGB'))
      processor = GameboyViewProcessor(image)
      continue_image = processor.get_continue()
      gameboy_image = GameboyImage(continue_image, 8, 4, 53, 53, is_tiled=True)
      gameboy_image.untile()
      number_process = NumberProcessor(gameboy_image.image)
      self.assertEqual(71006 ,number_process.get_number())

  def test_gameboy_image(self):
    processor = self.create_gameboy_view_processor()

    #get a tiled 4x4 image
    preview_image = processor.get_preview()

    gameboy_image = GameboyImage(preview_image, 4, 4, 53, 53, is_tiled=True)
    image = gameboy_image.untile()
    self.assertEqual(4*53, image.shape[0])
    self.assertEqual(4*53, image.shape[1])
    self.assertEqual(3, image.shape[2])

    image = gameboy_image.tile()
    self.assertEqual(4, image.shape[0])
    self.assertEqual(4, image.shape[1])
    self.assertEqual(53, image.shape[2])
    self.assertEqual(53, image.shape[3])
    self.assertEqual(3, image.shape[4])

  def create_gameboy_view_processor(self):
    return self.create_gameboy_view_processor_with("test/gameboy-full-view.png")

  def create_gameboy_view_processor_with(self, path):
    image = np.array(Image.open(path).convert('RGB'))
    return GameboyViewProcessor(image)

  def test_playfield_in_transition(self):
    processor = self.create_gameboy_view_processor_with("test/gameboy-full-view-in-transition.png")
    playfield_processor = PlayfieldProcessor(processor.get_playfield(), image_is_tiled=True)
    playfield = playfield_processor.run()
    self.assertTrue(playfield.in_transition)

  def test_playfield_in_transition_2(self):
    processor = self.create_gameboy_view_processor_with("test/gameboy-full-view-in-transition-2.png")
    playfield_processor = PlayfieldProcessor(processor.get_playfield(), image_is_tiled=True)
    playfield = playfield_processor.run()
    self.assertTrue(playfield.in_transition)

  def test_playfield_in_transition_3(self):
    processor = self.create_gameboy_view_processor_with("test/gameboy-full-view-in-transition-3.png")
    playfield_processor = PlayfieldProcessor(processor.get_playfield(), image_is_tiled=True)
    playfield = playfield_processor.run()
    self.assertTrue(playfield.in_transition)

  def test_playfield_in_transition_4(self):
    processor = self.create_gameboy_view_processor_with("test/gameboy-full-view-in-transition-4.png")
    playfield_processor = PlayfieldProcessor(processor.get_playfield(), image_is_tiled=True)
    playfield = playfield_processor.run()
    self.assertTrue(playfield.in_transition)

  def test_playfield_in_transition_5(self):
    # This does not work as the difference is too small.
    # Another approach is needed here. This only happens
    # shortly after a line clear
    processor = self.create_gameboy_view_processor_with("test/gameboy-full-view-in-transition-problematic.png")
    playfield_processor = PlayfieldProcessor(processor.get_playfield(), image_is_tiled=True)
    playfield = playfield_processor.run()
    self.assertTrue(playfield.in_transition)

  def test_playfield_line_clear(self):
    processor = self.create_gameboy_view_processor_with("test/gameboy-full-view-tetris.png")
    playfield_processor = PlayfieldProcessor(processor.get_playfield(), image_is_tiled=True)
    playfield = playfield_processor.run(save_tiles=True)
    self.assertEqual(1, playfield.line_clear_count)
    self.assertTrue(playfield.is_line_clear())

  def test_playfield_line_clear_2(self):
    processor = self.create_gameboy_view_processor_with("test/gameboy-full-view-tetris-2.png")
    playfield_processor = PlayfieldProcessor(processor.get_playfield(), image_is_tiled=True)
    playfield = playfield_processor.run(save_tiles=True)
    print(playfield.playfield_array)
    self.assertEqual(2, playfield.line_clear_count)
    self.assertTrue(playfield.is_line_clear())

  def test_playfield_non_line_clear(self):
    processor = self.create_gameboy_view_processor_with("test/gameboy-full-view-non-tetris.png")
    playfield_processor = PlayfieldProcessor(processor.get_playfield(), image_is_tiled=True)
    playfield = playfield_processor.run()
    self.assertEqual(0, playfield.line_clear_count)
    self.assertFalse(playfield.is_line_clear())

  def test_playfield_not_in_transition(self):
    processor = self.create_gameboy_view_processor_with("test/gameboy-full-view.png")
    playfield_processor = PlayfieldProcessor(processor.get_playfield(), image_is_tiled=True)
    playfield = playfield_processor.run()
    self.assertFalse(playfield.in_transition)

  def test_combine_gameboy_view_processor_and_other_processors(self):
    processor = self.create_gameboy_view_processor()

    preview_image = processor.get_preview()
    preview_processor = PreviewProcessor(preview_image, image_is_tiled=True)
    preview = preview_processor.run()
    self.assertEqual(preview, TileRecognizer.T_MINO)

    score = self.get_score(processor)
    self.assertEqual(39, score)

    lines = self.get_lines(processor)
    self.assertEqual(0, lines)

    level = self.get_level(processor)
    self.assertEqual(0, level)

    playfield_image = processor.get_playfield()

  def test_stats_image(self):
    stat = StatsImage()
    stat.create_image([0, 1, 10, 200, 2, 5, 7])

  def get_level(self, processor):
    level_image = processor.get_level()
    level = self.get_number(level_image)
    return level

  def get_number(self, number_image, save_image=False):
    number_image = GameboyImage(number_image, number_image.shape[0], number_image.shape[1],
                                number_image.shape[2], number_image.shape[3], is_tiled=True)
    number_image.untile()
    if(save_image):
      cv2.imwrite("test/number.png", number_image.image)

    number_processor = NumberProcessor(number_image.image)
    level = number_processor.get_number()
    return level

  def get_lines(self, processor, save_image=False):
    lines_image = processor.get_lines()
    lines = self.get_number(lines_image, save_image)
    return lines

  def get_score(self, processor):
    score_image = processor.get_score()
    score = self.get_number(score_image)
    return score

  def test_number_processor_score_99(self):
    processor = self.create_gameboy_view_processor_with("test/gameboy-full-view-problematic-score.png")
    self.assertEqual(99, self.get_score(processor))

  def test_number_processor_score_98(self):
    # Currently not fixable
    image = self.get_image("test/numbers/98.png")
    processor = NumberProcessor(image)
    result = processor.get_number()
    self.assertEqual(98, result)

  def test_sequential_number_processor_score_98(self):
    image = self.get_tiled_image("test/numbers/98.png", 1, 6, 48, 48)
    processor = SequentialNumberProcessor(image)
    result = processor.get_number()
    self.assertEqual(98, result)

  def test_number_processor_score_9(self):
    image = self.get_image("test/numbers/9.png")
    processor = NumberProcessor(image)
    result = processor.get_number()
    self.assertEqual(9, result)

  def test_sequential_number_processor_score_9(self):
    image = self.get_tiled_image("test/numbers/9.png", 1, 3, 35, 35)
    processor = SequentialNumberProcessor(image)
    result = processor.get_number()
    self.assertEqual(9, result)

  def test_number_processor_score_15600(self):
    image = self.get_image("test/numbers/15600.png")
    processor = NumberProcessor(image)
    result = processor.get_number()
    self.assertEqual(15600, result)

  def test_sequential_number_processor_score_15600(self):
    image = self.get_tiled_image("test/numbers/15600.png", 1, 6, 48, 48)
    processor = SequentialNumberProcessor(image)
    result = processor.get_number()
    self.assertEqual(15600, result)

  def test_number_processor_score_19083(self):
    image = self.get_image("test/numbers/19083.png")
    processor = NumberProcessor(image)
    result = processor.get_number()
    self.assertEqual(19083, result)

  def test_sequential_number_processor_score_19083(self):
    image = self.get_tiled_image("test/numbers/19083.png", 1, 6, 48, 48)
    processor = SequentialNumberProcessor(image)
    result = processor.get_number()
    self.assertEqual(19083, result)

  def test_number_processor_score_102839(self):
    image = self.get_image("test/numbers/102839.png")
    processor = NumberProcessor(image)
    result = processor.get_number()
    self.assertEqual(102839, result)

  def test_sequential_number_processor_score_102839(self):
    image = self.get_tiled_image("test/numbers/102839.png", 1, 6, 48, 48)
    processor = SequentialNumberProcessor(image)
    result = processor.get_number()
    self.assertEqual(102839, result)

  def test_number_processor_score_12097(self):
    image = self.get_image("test/numbers/12097.png")
    processor = NumberProcessor(image)
    result = processor.get_number()
    self.assertEqual(12097, result)

  def test_sequential_number_processor_score_12097(self):
    image = self.get_tiled_image("test/numbers/12097.png", 1, 6, 48, 48)
    processor = SequentialNumberProcessor(image)
    result = processor.get_number()
    self.assertEqual(12097, result)

  def test_problematic_level(self):
    processor = self.create_gameboy_view_processor_with("test/gameboy-full-view-problematic-score.png")
    self.assertEqual(9, self.get_level(processor))

  def test_problematic_lines(self):
    # Currently not fixable
    processor = self.create_gameboy_view_processor_with("test/gameboy-full-view-problematic-lines.png")
    self.assertEqual(9, self.get_lines(processor))

  def test_gameboy_view_processor(self):
      processor = self.create_gameboy_view_processor()

      playfield = processor.get_playfield()
      self.assertEqual(playfield.shape[0], 18)
      self.assertEqual(playfield.shape[1], 10)

      preview = processor.get_preview()
      self.assertEqual(preview.shape[0], 4)
      self.assertEqual(preview.shape[1], 4)

      score = processor.get_score()
      self.assertEqual(score.shape[0], 1)
      self.assertEqual(score.shape[1], 6)

      lines = processor.get_lines()
      self.assertEqual(lines.shape[0], 1)
      self.assertEqual(lines.shape[1], 3)

  def test_l_mino(self):
    recognizer = TileRecognizer()
    tile = np.array(Image.open("test/tiles/L-mino-1.png").convert('RGB'))
    result = recognizer.recognize(tile)

    self.assertEqual(result, 3)

  def test_t_mino(self):
    recognizer = TileRecognizer()
    tile = np.array(Image.open("test/tiles/T-mino-1.png").convert('RGB'))

    result = recognizer.recognize(tile)

    self.assertEqual(result, 4)

  def test_tiler(self):
    image = np.array(Image.open("test/scenario-2-high-res.png").convert('RGB'))
    tiler = Tiler(18, 10, image)
    assert(tiler.adapted_image.shape[0] == 18)
    assert(tiler.adapted_image.shape[1] == 10)
    self.assertEqual(tiler.tile_height, 53)
    self.assertEqual(tiler.tile_width, 53)

  def test_preview_processor_4x4tiles(self):
    image = np.array(Image.open("test/preview/t-to-l-tetromino-transition-preview.png").convert('RGB'))
    preview_processor = PreviewProcessor(image)
    self.assertEqual(4, preview_processor.nr_of_tiles_height)
    self.assertEqual(4, preview_processor.nr_of_tiles_width)

  def test_preview_processor_ambigous(self):
    image = np.array(Image.open("test/preview/t-to-l-tetromino-transition-preview.png").convert('RGB'))
    preview_processor = PreviewProcessor(image)
    preview_processor.run()
    self.assertTrue(preview_processor.ambigous)

  def test_preview_processor_z(self):
    image = np.array(Image.open("test/preview/z-tetromino-preview.png").convert('RGB'))
    preview_processor = PreviewProcessor(image)
    result = preview_processor.run(save_tiles=True)
    self.assertEqual(result, TileRecognizer.Z_MINO)
    self.assertFalse(preview_processor.ambigous)

  def test_preview_processor_l(self):
    image = np.array(Image.open("test/preview/l-tetromino-preview.png").convert('RGB'))
    preview_processor = PreviewProcessor(image)
    result = preview_processor.run()
    self.assertEqual(result, TileRecognizer.L_MINO)
    self.assertFalse(preview_processor.ambigous)

  def test_preview_processor_j(self):
    image = np.array(Image.open("test/preview/j-tetromino-preview.png").convert('RGB'))
    preview_processor = PreviewProcessor(image)
    result = preview_processor.run()
    self.assertEqual(result, TileRecognizer.J_MINO)
    self.assertFalse(preview_processor.ambigous)

  def test_preview_processor_s(self):
    image = np.array(Image.open("test/preview/s-tetromino-preview.png").convert('RGB'))
    preview_processor = PreviewProcessor(image)
    result = preview_processor.run()
    self.assertEqual(result, TileRecognizer.S_MINO)
    self.assertFalse(preview_processor.ambigous)

  def test_preview_processor_o(self):
    image = np.array(Image.open("test/preview/o-tetromino-preview.png").convert('RGB'))
    preview_processor = PreviewProcessor(image)
    result = preview_processor.run()
    self.assertEqual(result, TileRecognizer.O_MINO)
    self.assertFalse(preview_processor.ambigous)

  def test_preview_processor_i(self):
    image = np.array(Image.open("test/preview/i-tetromino-preview.png").convert('RGB'))
    preview_processor = PreviewProcessor(image)
    result = preview_processor.run()
    self.assertEqual(result, TileRecognizer.I_MINO_SIMPLE)
    self.assertFalse(preview_processor.ambigous)

  def test_perfect_score(self):
    plotter = Plotter()
    scores, lines = plotter.get_perfect_score_table()
    plotter.show_plot(scores, lines)
    self.assertTrue(scores[-1], 1401300);

  def test_worst_score(self):
    plotter = Plotter()
    scores, lines = plotter.get_worst_score_table()
    plotter.show_plot(scores, lines)
    self.assertTrue(len(scores), 300);

  def test_preview_processor_t(self):
    image = np.array(Image.open("test/preview/t-tetromino-preview.png").convert('RGB'))
    preview_processor = PreviewProcessor(image)
    result = preview_processor.run()
    self.assertEqual(result, TileRecognizer.T_MINO)
    self.assertFalse(preview_processor.ambigous)

  def test_playfield_recreator(self):
    recreator = PlayfieldRecreator()
    playfield = self.create_testing_array_s2()
    recreator.recreate(playfield, 'test/screenshot-playfield-recreation.png')

  def test_csvreader(self):
    reader = CSVReader("20230511110411", path="test/csv/")
    reader.to_image("test/recreation/")

  def full_image(self, image_path, test):
    image = np.array(Image.open(image_path).convert('RGBA'))
    playfield = PlayfieldProcessor(image)
    result = playfield.run().playfield_array
    self.performance(result, test)

  def performance(self, result, test):
    difference = result - test
    hits = result.copy()
    # set edge cases to no tile
    hits[hits > 11] = -99
    hits[hits > -99] = 1
    hits[hits == -99] = 0
    hits = hits - self.create_array_only_hits(test)
    false_negatives = hits.copy()
    false_negatives[hits == 1] = 0
    false_negatives[hits == -1] = 1
    performance = np.sum(false_negatives)
    self.assertEqual(0, performance, "Some false negatives")

    false_positives = hits.copy()
    false_positives[hits == -1] = 0
    performance = np.sum(false_positives)

    if (performance > 0):
      print(result)
      print(difference)

    self.assertEqual(0, performance, "Some false positives")

    arr = difference.copy()
    arr[arr > 0] = 1
    arr[arr < 0] = 1

    performance = np.sum(arr)
    if (performance > 0):
      print(arr)
    self.assertEqual(0, performance, "Some miscategorized minos")

  def test_full_view(self):
    image = self.get_image("test/gameboy-full-view.png")
    processor = GameboyViewProcessor(image)
    playfield_image = processor.get_playfield()
    playfield = PlayfieldProcessor(playfield_image, image_is_tiled=True).run(save_tiles=True).playfield_array
    self.performance(playfield, self.create_testing_array_full_view())

  def test_full_view_2(self):
    image = self.get_image("test/gameboy-full-view-2.png")
    processor = GameboyViewProcessor(image)
    playfield_image = processor.get_playfield()
    playfield = PlayfieldProcessor(playfield_image, image_is_tiled=True).run(save_tiles=True).playfield_array
    self.performance(playfield, self.create_testing_array_full_view_2())

  def get_image(self, path):
    return cv2.imread(path)

  def get_tiled_image(self, path, number_of_tiles_height, number_of_tiles_width, tile_height, tile_width):
    image = self.get_image(path)
    gb_image = GameboyImage(image, number_of_tiles_height, number_of_tiles_width, tile_height, tile_width, is_tiled=False)
    return gb_image.tile()

  def test_second_scenario(self):
    self.full_image("test/scenario-2-high-res.png", self.create_testing_array_s2())

  def test_first_scenario(self):
    self.full_image("test/scenario-1-high-res.png", self.create_testing_array_s1())

  def create_testing_array_full_view(self):
    array = [[-99, -99, -99, -99, -99, -99, -99, -99, -99, -99],
             [-99, -99, -99, -99, -99, -99, -99, -99, -99, -99],
             [-99, -99, -99, -99, -99, -99, -99, -99, -99, -99],
             [-99, -99, -99, -99, -99, -99, -99, -99, -99, -99],
             [-99, -99, -99, -99, -99, -99, -99, -99, -99, -99],
             [-99, -99, -99, -99, -99, -99, -99, -99, -99, -99],
             [-99, -99, -99, -99, -99, -99, -99, -99, -99, -99],
             [-99, -99, -99,   1,   1, -99, -99, -99, -99, -99],
             [-99, -99, -99, -99,   1,   1, -99, -99, -99, -99],
             [  0,   0,   0, -99, -99, -99, -99, -99, -99, -99],
             [-99, -99,   0, -99, -99, -99, -99, -99, -99, -99],
             [  3,   3,   3,   9,  10,  10,  11, -99, -99, -99],
             [  3, -99, -99,   4,   4,   4, -99, -99, -99, -99],
             [  4, -99, -99, -99,   4, -99, -99,   1,   1, -99],
             [  4,   4, -99,   3,   3,   3, -99, -99,   1,   1],
             [  4, -99, -99,   3, -99, -99, -99, -99, -99,   4],
             [  2,   2, -99,   1,   1, -99, -99, -99,   4,   4],
             [  2,   2, -99, -99,   1,   1, -99, -99, -99,   4]]
    return (np.array(array))

  def create_testing_array_full_view_2(self):
    array = [[-99, -99, -99, -99, -99, -99, -99, -99, -99, -99],
             [-99, -99, -99, -99, -99, -99, -99, -99, -99, -99],
             [-99, -99, -99, -99, -99, -99, -99, -99, -99, -99],
             [-99,   6, -99, -99, -99, -99, -99, -99, -99, -99],
             [-99,   7, -99, -99, -99, -99, -99, -99, -99, -99],
             [-99,   7, -99, -99, -99, -99, -99, -99, -99, -99],
             [-99,   8, -99, -99, -99, -99, -99, -99, -99, -99],
             [-99, -99, -99, -99, -99, -99, -99, -99, -99, -99],
             [-99, -99, -99, -99, -99, -99, -99, -99, -99, -99],
             [-99, -99, -99, -99, -99, -99, -99, -99, -99, -99],
             [-99, -99, -99, -99, -99, -99, -99, -99, -99, -99],
             [-99, -99, -99, -99, -99, -99, -99, -99, -99, -99],
             [-99, -99, -99, -99, -99, -99, -99, -99, -99,   6],
             [-99, -99, -99, -99, -99, -99, -99, -99, -99,   7],
             [-99, -99, -99, -99,   5, -99, -99, -99, -99,   7],
             [-99, -99, -99, -99,   5,   5, -99,   4, -99,   8],
             [-99, -99,   3,   3,   3,   5,   4,   4,   2,   2],
             [-99, -99,   3,   9,  10,  10,  11,   4,   2,   2]]
    return (np.array(array))

  def create_testing_array_s2(self):
    array = [ [ -99 , -99 , -99 , -99 , -99, -99, -99, -99, -99, -99 ],
              [ -99 , -99 , -99 ,   3 ,   3,   3, -99, -99, -99, -99 ],
              [ -99 , -99 , -99 ,   3 , -99, -99, -99, -99, -99, -99 ],
              [ -99 , -99 , -99 , -99 ,   2,   2, -99, -99, -99,   4 ],
              [ -99 , -99 , -99 , -99 ,   2,   2, -99,   5,   4,   4 ],
              [ -99 ,   2 ,   2 , -99 ,   5,   5, -99,   5,   5,   4 ],
              [ -99 ,   2 ,   2 ,   5 ,   5, -99,   5,   5,   5, -99 ],
              [ -99 , -99 ,   1 ,   1 , -99,   5,   5, -99, -99, -99 ],
              [ -99 , -99 , -99 ,   1 ,   1,   1, -99, -99, -99, -99 ],
              [ -99 , -99 , -99 , -99 ,   1,   1, -99, -99, -99, -99 ],
              [ -99 , -99 , -99 , -99 ,   1, -99, -99, -99, -99, -99 ],
              [ -99 , -99 , -99 , -99 ,   2,   2, -99, -99, -99, -99 ],
              [ -99 , -99 , -99 , -99 ,   2,   2, -99, -99, -99, -99 ],
              [ -99 , -99 , -99 , -99 ,   3,   3, -99, -99, -99, -99 ],
              [ -99 , -99 , -99 , -99 , -99,   3, -99, -99, -99, -99 ],
              [ -99 , -99 , -99 , -99 , -99,   3, -99, -99,   2,   2 ],
              [ -99 , -99 , -99 , -99 ,   1,   1, -99, -99,   2,   2 ],
              [ -99 , -99 ,   5 , -99 ,   6,   1,   1, -99,   2,   2 ] ]
    return (np.array(array))

  def create_testing_array_s2_without_dropping_piece(self):
    array = [[-99, -99, -99, -99, -99, -99, -99, -99, -99, -99],
             [-99, -99, -99, -99, -99, -99, -99, -99, -99, -99],
             [-99, -99, -99, -99, -99, -99, -99, -99, -99, -99],
             [-99, -99, -99, -99, 2, 2, -99, -99, -99, 4],
             [-99, -99, -99, -99, 2, 2, -99, 5, 4, 4],
             [-99, 2, 2, -99, 5, 5, -99, 5, 5, 4],
             [-99, 2, 2, 5, 5, -99, 5, 5, 5, -99],
             [-99, -99, 1, 1, -99, 5, 5, -99, -99, -99],
             [-99, -99, -99, 1, 1, 1, -99, -99, -99, -99],
             [-99, -99, -99, -99, 1, 1, -99, -99, -99, -99],
             [-99, -99, -99, -99, 1, -99, -99, -99, -99, -99],
             [-99, -99, -99, -99, 2, 2, -99, -99, -99, -99],
             [-99, -99, -99, -99, 2, 2, -99, -99, -99, -99],
             [-99, -99, -99, -99, 3, 3, -99, -99, -99, -99],
             [-99, -99, -99, -99, -99, 3, -99, -99, -99, -99],
             [-99, -99, -99, -99, -99, 3, -99, -99, 2, 2],
             [-99, -99, -99, -99, 1, 1, -99, -99, 2, 2],
             [-99, -99, 5, -99, 6, 1, 1, -99, 2, 2]]
    return (np.array(array))

  def create_testing_array_s2_next_piece(self):
    """
    This example was artificially created by hand
    """
    array = [ [ -99 , -99 , -99 , -99 , -99, -99, -99, -99, -99, -99 ],
              [ -99 , -99 , -99 , -99 ,   5,   5, -99, -99, -99, -99 ],
              [ -99 , -99 , -99 ,   5 ,   5, -99, -99, -99, -99, -99 ],
              [ -99 , -99 , -99 , -99 ,   2,   2, -99, -99, -99,   4 ],
              [   3 ,   3 ,   3 , -99 ,   2,   2, -99,   5,   4,   4 ],
              [   3 ,   2 ,   2 , -99 ,   5,   5, -99,   5,   5,   4 ],
              [ -99 ,   2 ,   2 ,   5 ,   5, -99,   5,   5,   5, -99 ],
              [ -99 , -99 ,   1 ,   1 , -99,   5,   5, -99, -99, -99 ],
              [ -99 , -99 , -99 ,   1 ,   1,   1, -99, -99, -99, -99 ],
              [ -99 , -99 , -99 , -99 ,   1,   1, -99, -99, -99, -99 ],
              [ -99 , -99 , -99 , -99 ,   1, -99, -99, -99, -99, -99 ],
              [ -99 , -99 , -99 , -99 ,   2,   2, -99, -99, -99, -99 ],
              [ -99 , -99 , -99 , -99 ,   2,   2, -99, -99, -99, -99 ],
              [ -99 , -99 , -99 , -99 ,   3,   3, -99, -99, -99, -99 ],
              [ -99 , -99 , -99 , -99 , -99,   3, -99, -99, -99, -99 ],
              [ -99 , -99 , -99 , -99 , -99,   3, -99, -99,   2,   2 ],
              [ -99 , -99 , -99 , -99 ,   1,   1, -99, -99,   2,   2 ],
              [ -99 , -99 ,   5 , -99 ,   6,   1,   1, -99,   2,   2 ] ]
    return (np.array(array))

  def create_testing_array_s1(self):
    array = [ [ -99 , -99 , -99 , -99 , -99, -99, -99, -99, -99, -99 ],
              [ -99 , -99 , -99 , -99 , -99, -99, -99, -99, -99, -99 ],
              [ -99 , -99 , -99 , -99 , -99, -99, -99, -99, -99, -99 ],
              [ -99 , -99 , -99 , -99 , -99, -99, -99, -99, -99, -99 ],
              [ -99 , -99 , -99 , -99 , -99, -99, -99, -99, -99, -99 ],
              [ -99 , -99 , -99 , -99 , -99, -99, -99, -99, -99, -99 ],
              [ -99 , -99 , -99 , -99 , -99, -99, -99, -99, -99, -99 ],
              [ -99 , -99 , -99 ,   1 ,   1, -99, -99, -99, -99, -99 ],
              [ -99 , -99 , -99 , -99 ,   1,   1, -99, -99, -99, -99 ],
              [   0 ,   0 ,   0 , -99 , -99, -99, -99, -99, -99, -99 ],
              [ -99 , -99 ,   0 , -99 , -99, -99, -99, -99, -99, -99 ],
              [   3 ,   3 ,   3 ,   9 ,  10,  10,  11, -99, -99, -99 ],
              [   3 , -99 , -99 ,   4 ,   4,   4, -99, -99, -99, -99 ],
              [   4 , -99 , -99 , -99 ,   4, -99, -99,   1,   1, -99 ],
              [   4 ,   4 , -99 ,   3 ,   3,   3, -99, -99,   1,   1 ],
              [   4 , -99 , -99 ,   3 , -99, -99, -99, -99, -99,   4 ],
              [   2 ,   2 , -99 ,   1 ,   1, -99, -99, -99,   4,   4 ],
              [   2 ,   2 , -99 , -99 ,   1,   1, -99, -99, -99,   4 ] ]
    return (np.array(array))

  def create_testing_array_high_parity(self):
    array = [ [-99, -99, -99, -99, -99, -99, -99, -99, -99, -99],
              [-99, -99, -99, -99, -99, -99, -99, -99, -99, -99],
              [-99, -99, -99, -99, -99, -99, -99, -99, -99, -99],
              [-99, -99, -99, -99, -99, -99, -99, -99, -99, -99],
              [-99, -99, -99, -99, -99, -99, -99, -99, -99, -99],
              [-99, -99, -99, -99, -99, -99, -99, -99, -99, -99],
              [-99, -99, -99, -99, -99, -99, -99, -99, -99, -99],
              [-99, -99, -99, -99, -99, -99, -99, -99, -99, -99],
              [-99, -99, -99, -99, -99, -99, -99, -99, -99, -99],
              [-99, -99, -99, -99, -99, -99, -99, -99, -99, -99],
              [-99, -99, -99, -99, -99, -99, -99, -99, -99, -99],
              [-99, -99, -99, -99, -99, -99, -99, -99, -99, -99],
              [-99, -99, -99, -99, -99, -99, -99, -99, -99, -99],
              [-99, -99, -99, -99, -99, -99, -99, -99, -99, -99],
              [-99, -99, -99, -99, -99, -99, -99, -99, -99, -99],
              [-99, -99, -99, -99, -99, -99, -99, -99, -99, -99],
              [-99, -99, -99, -99,   4, -99, -99, -99,   4, -99],
              [-99, -99, -99,   4,   4,   4, -99,   4,   4,   4], ]
    return (np.array(array))

  def create_testing_array_full_line_grey(self):
    array = [ [ -99 , -99 , -99 , -99 , -99, -99, -99, -99, -99, -99 ],
              [ -99 , -99 , -99 , -99 , -99, -99, -99, -99, -99, -99 ],
              [ -99 , -99 , -99 , -99 , -99, -99, -99, -99, -99, -99 ],
              [ -99 , -99 , -99 , -99 , -99, -99, -99, -99, -99, -99 ],
              [ -99 , -99 , -99 , -99 , -99, -99, -99, -99, -99, -99 ],
              [ -99 , -99 , -99 , -99 , -99, -99, -99, -99, -99, -99 ],
              [ -99 , -99 , -99 , -99 , -99, -99, -99, -99, -99, -99 ],
              [ -99 , -99 , -99 , -99 , -99, -99, -99, -99, -99, -99 ],
              [ -99 , -99 , -99 , -99 , -99,  -99, -99, -99, -99, -99 ],
              [   0 ,   0 ,   0 , -99 , -99, -99, -99, -99, -99, -99 ],
              [ -99 , -99 ,   0 , -99 , -99, -99, -99, -99, -99, -99 ],
              [  12 ,  12 ,  12 ,  12 ,  12,  12,  12,  12,  12,  12 ],
              [   3 , -99 , -99 ,   4 ,   4,   4, -99,   3, -99, -99 ],
              [   4 , -99 , -99 , -99 ,   4, -99, -99,   1,   1, -99 ],
              [   4 ,   4 , -99 ,   3 ,   3,   3, -99, -99,   1,   1 ],
              [   4 , -99 , -99 ,   3 , -99, -99, -99, -99, -99,   4 ],
              [   2 ,   2 , -99 ,   1 ,   1, -99, -99, -99,   4,   4 ],
              [   2 ,   2 , -99 , -99 ,   1,   1, -99, -99, -99,   4 ] ]
    return (np.array(array))


  def create_testing_array_full_line(self):
    array = [ [ -99 , -99 , -99 , -99 , -99, -99, -99, -99, -99, -99 ],
              [ -99 , -99 , -99 , -99 , -99, -99, -99, -99, -99, -99 ],
              [ -99 , -99 , -99 , -99 , -99, -99, -99, -99, -99, -99 ],
              [ -99 , -99 , -99 , -99 , -99, -99, -99, -99, -99, -99 ],
              [ -99 , -99 , -99 , -99 , -99, -99, -99, -99, -99, -99 ],
              [ -99 , -99 , -99 , -99 , -99, -99, -99, -99, -99, -99 ],
              [ -99 , -99 , -99 , -99 , -99, -99, -99, -99, -99, -99 ],
              [ -99 , -99 , -99 , -99 , -99, -99, -99, -99, -99, -99 ],
              [ -99 , -99 , -99 , -99 , -99,  -99, -99, -99, -99, -99 ],
              [   0 ,   0 ,   0 , -99 , -99, -99, -99, -99, -99, -99 ],
              [ -99 , -99 ,   0 , -99 , -99, -99, -99, -99, -99, -99 ],
              [   3 ,   3 ,   3 ,   9 ,  10,  10,  11,   3,   3,   3 ],
              [   3 , -99 , -99 ,   4 ,   4,   4, -99,   3, -99, -99 ],
              [   4 , -99 , -99 , -99 ,   4, -99, -99,   1,   1, -99 ],
              [   4 ,   4 , -99 ,   3 ,   3,   3, -99, -99,   1,   1 ],
              [   4 , -99 , -99 ,   3 , -99, -99, -99, -99, -99,   4 ],
              [   2 ,   2 , -99 ,   1 ,   1, -99, -99, -99,   4,   4 ],
              [   2 ,   2 , -99 , -99 ,   1,   1, -99, -99, -99,   4 ] ]
    return (np.array(array))

  def create_array_only_hits(self, array):
    array = array.copy()
    array[array > -99] = 1
    array[array == -99] = 0
    return array

if __name__ == '__main__':
  unittest.main()