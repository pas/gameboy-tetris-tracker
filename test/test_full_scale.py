import unittest
from queue import Queue
from unittest.mock import patch, MagicMock

from tetristracker.capturer.video_file_capturer import VideoFileCapturer
from tetristracker.game import Round
from tetristracker.storage.writer import Writer
from tetristracker.runner import Runner
from tetristracker.tile.mino import Mino
from tetristracker.workers.get.gameboy_view_processor_to_playfield_processor import \
  GameboyViewProcessorToPlayfieldProcessor
from tetristracker.workers.get.image_capture import ImageCapture
from tetristracker.workers.get.image_to_gameboy_view_processor import ImageToGameboyViewProcessor
from tetristracker.workers.steppers.queue_stepper import QueueStepper

class TestFullScale(unittest.TestCase):
  def test_full_scale_video(self):
    """
    Does a full scale test along a video
    file. Not finished yet!
    """

    # image capture
    file_name = "test/video/video-test-full-68.mkv"
    bounding_box = {"height": 467, "left": 73, "top": 127, "width": 518}
    capturer = VideoFileCapturer(file_name, bounding_box)
    capture_get = ImageCapture(capturer)
    images_queue = Queue()
    capture_stepper = QueueStepper(images_queue, capture_get)

    # gameboy view
    gb_view_get = ImageToGameboyViewProcessor(False, images_queue)
    gb_view_queue = Queue()
    gb_view_stepper = QueueStepper(gb_view_queue, gb_view_get)

    # playfield
    playfield_get = GameboyViewProcessorToPlayfieldProcessor(gb_view_queue)
    playfield_queue = Queue()
    playfield_stepper = QueueStepper(playfield_queue, playfield_get)

    class GameMock():
      def __init__(self):
        self.counter = 0

      def get_gameboy_view_processor(self):
        capture_stepper.step()
        gb_view_stepper.step()
        playfield_stepper.step()
        self.counter += 1
        print("")
        print("------")
        print("Counter: " + str(self.counter))
        return playfield_queue.get()

      def is_running(self, _):
        return True

      def force_stop(self):
        return False

    score_progression = [0, 7, 17, 26, 40, 47, 52, 57, 61, 64, 68]
    tetromino_progression = "TTSILSLTOLZZJZLISSOOSOTL"

    class QueueMock():
      def __init__(self, test):
        self.score_index = 0
        self.preview_index = 0
        self.spawned_index = 0
        self.test = test

      def test_score(self, score):
        if score == score_progression[self.score_index] or score == - 1:
          return

        self.score_index += 1

        if score == score_progression[self.score_index]:
          return

        self.test.fail("For score nr. " + str(self.score_index+1) + " expected " + str(score_progression[self.score_index]) + " but got " + str(score) + ".")

      def test_preview(self, tetromino_in_preview):
        if len(tetromino_progression) <= self.preview_index:
          return

        if Mino.number_to_short_name_array[tetromino_in_preview] == tetromino_progression[self.preview_index] or tetromino_in_preview == - 1:
          return

        self.preview_index += 1

        if len(tetromino_progression) <= self.preview_index:
          return

        # its fine if it is still the same. We can't spot changes in preview if the mino stays the same
        while tetromino_progression[self.preview_index-1] == tetromino_progression[self.preview_index]:
          self.preview_index += 1

        if Mino.number_to_short_name_array[tetromino_in_preview] == tetromino_progression[self.preview_index]:
          return

        self.test.fail("For tetromino in preview at index " + str(self.preview_index) + " expected " + tetromino_progression[self.preview_index] + " but got " + Mino.number_to_short_name_array[tetromino_in_preview] + ".")

      def test_spawning(self, spawned_tetromino, just_spawned):
        print(Mino.number_to_short_name_array[spawned_tetromino])
        print(just_spawned)
        if(just_spawned):
          if Mino.number_to_short_name_array[spawned_tetromino] == tetromino_progression[self.spawned_index]:
            self.spawned_index += 1
            return

          self.test.fail("For spawned element nr. " + str(self.spawned_index+1) + " expected " + tetromino_progression[self.spawned_index] + " but got " + Mino.number_to_short_name_array[spawned_tetromino]  + ".")

      def put(self, res):
        plotter, result = res
        score, lines, level, tetromino_in_preview, spawned_tetromino, just_spawned, playfield = result
        self.test_score(score)
        self.test.assertEqual(lines, 0) # lines do not change here. they stay 0
        self.test.assertEqual(level, 9) # level does not change here. it stays level 9
        self.test_preview(tetromino_in_preview)
        self.test_spawning(spawned_tetromino, just_spawned)



    game = GameMock()
    queue = QueueMock(self)
    processor, playfield = game.get_gameboy_view_processor()

    round = Round(game, None, queue)
    try:
      round.start(processor, playfield)
    except EOFError:
      pass



