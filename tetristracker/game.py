import threading
import time
from abc import abstractmethod
from queue import Queue

import cv2
import numpy as np
from PIL import ImageOps
from PIL import Image

from tetristracker.capturer.capture_selection import CaptureSelection
from tetristracker.commasv.writer import Writer
from tetristracker.helpers.config import Config
from tetristracker.image.gameboy_image import GameboyImage
from tetristracker.processor.gameboy_view_processor import GameboyViewProcessor
from tetristracker.image.image_saver import ImageSaver
from tetristracker.processor.number_processor import SequentialNumberProcessor
from tetristracker.processor.playfield_processor import PlayfieldProcessor
from tetristracker.stats.stats import Stats
from tetristracker.tile.tile import Tile
from tetristracker.unit.playfield import Playfield
from tetristracker.processor.preview_processor import SpawningProcessor, PreviewProcessor
from tetristracker.tracker.preview_tracker import PreviewTracker
from tetristracker.tracker.level_tracker import LevelTracker
from tetristracker.tracker.lines_tracker import LinesTracker
from tetristracker.tracker.score_tracker import ScoreTracker
from tetristracker.tracker.playfield_tracker import PlayfieldTracker
from tetristracker.helpers.timer import Timer
from tetristracker.global_vars import images_queue, gameboyview_queue


class Get():
  @abstractmethod
  def get(self):
    pass


def put_queue(queue: Queue, callable: Get, time_it=False):
  while (True):
    if time_it: start_run = time.perf_counter()

    queue.put(callable.get())

    if time_it: end_run = time.perf_counter()
    if time_it: print("Passed per run: " + str(end_run - start_run))


class ImageCaptureGet(Get):
  def __init__(self):
    config = Config()

    # create capturer (this seems to have to be inside
    # the local thread or else mss doesn't work)
    capture_selection = CaptureSelection(config)
    capture_selection.select(config.get_capturer())

    capturer = capture_selection.get()

    self.capturer = capturer

  def get(self):
    return self.capturer.grab_image()


class GameboyViewGet(Get):
  def __init__(self, shift_score, i_queue):
    self.i_queue = images_queue
    self.shift_score = shift_score
    self.saver = ImageSaver("screenshots/debug/", "retrieved")

  def get(self):
    image = self.i_queue.get()
    self.i_queue.task_done()
    self.saver.save(image)
    view = GameboyViewProcessor(image, shift_score=self.shift_score)
    return view


def capture():
  """
  Capturing images and put them into the
  queue
  """
  getter = ImageCaptureGet()
  put_queue(images_queue, getter, time_it=False)


def prepare(shift_score):
  """
  Prepare the captured images inside the queue.
  Put result into queue.
  """
  getter = GameboyViewGet(shift_score, images_queue)
  put_queue(gameboyview_queue, getter, time_it=True)


class Game:
  MIN_WAIT_TIME = 50

  def __init__(self, capturer, plotter, writer, shift_score=False):
    self.round = None
    self.capturer = capturer
    self.timer = Timer()
    self.plotter = plotter
    self.writer = writer
    self.shift_score = shift_score  # I really don't like this here :(

  def is_running(self, processor):
    """
    If the left top image is more or less
    black, then the game shows is in
    play state.
    """
    # This needs to be the passed processor
    # or else we can't use this method from
    # within Round (or we have to set it
    # up differently...)
    tile = processor.get_top_left_tile()
    # cv2.imwrite("direct_image.png", processor.original_image)
    # cv2.imwrite("direct_tile.png", tile.tile_image)
    return tile.is_black()

  def force_stop(self):
    thread = threading.current_thread()
    if callable(getattr(thread, "stopped", None)):
      return thread.stopped()
    else:
      return False

  def get_gameboy_view_processor(self):
    view = gameboyview_queue.get()
    gameboyview_queue.task_done()
    return view

  def state_machine(self):
    while not self.force_stop():
      if (self.is_running(self.processor)):
        self.run()
      else:
        self.idle()

  def run(self):
    """
    This starts three threads:
    1) Capture: Continuously capture images through the
    provided capturer and puts the into the queue
    2) Prepare: Fetches the grabbed image from the
    queue and prepares by using tile recognition.
    Drops unreliable images.
    Puts the array with the recognized tiles into
    another queue
    3) Analyse: Fetches results from queue and analysis the
    results
    """
    saver = ImageSaver("screenshots/debug/", "running")
    self.round = Round(self, saver, self.plotter, self.writer)
    self.round.start(self.processor)
    self.processor = self.get_gameboy_view_processor()

  def _empty_queues(self):
    # Before each new game we clear the global queues
    with images_queue.mutex:
      images_queue.queue.clear()

    with gameboyview_queue.mutex:
      gameboyview_queue.clear()

  def _start_capture_thread(self):
    # Start capturing thread
    t = threading.Thread(target=capture, daemon=True, name="capture")
    t.start()

  def _start_prepare_thread(self, shift_score):
    t = threading.Thread(target=prepare, args=(shift_score,), daemon=True, name="prepare")
    t.start()

  def start(self):
    self._start_capture_thread()
    self._start_prepare_thread(self.shift_score)

    self.processor = self.get_gameboy_view_processor()
    self.state_machine()

  def idle(self):
    """
    During idle stat we are regularly checking if
    another round has started. As soon as this is
    the case change state
    :return:
    """
    self.timer.start()
    while not self.is_running(self.processor) and not self.force_stop():
      self.processor = self.get_gameboy_view_processor()
      self.timer.wait_then_restart()


class Round:
  def __init__(self, game, saver, plotter, writer: Writer):
    self.csv_file = writer
    self.csv_file.restart()

    self.start_scores = 0
    self.start_lines = 0
    self.start_level = 0

    self.score_tracker: ScoreTracker = ScoreTracker()
    self.lines_tracker: LinesTracker = LinesTracker()
    self.level_tracker: LevelTracker = LevelTracker()
    self.preview_tracker: PreviewTracker = PreviewTracker()
    self.playfield_tracker: PlayfieldTracker = PlayfieldTracker()
    self.stats = Stats()
    self.saver = saver
    self.plotter = plotter
    self.game = game
    self.timer = Timer()

  def preview(self, processor):
    """
    Returns -1 if results are ambigous
    """
    preview_image = processor.get_preview()
    preview_processor = PreviewProcessor(preview_image, image_is_tiled=True)
    result = preview_processor.run()
    if (preview_processor.ambiguous):
      result = None
    return result

  def spawning(self, processor):
    """
    This never worked out because the piece does not
    stay long enough in the spawning area
    """
    spawning_image = processor.get_spawning_area()
    spawning_processor = SpawningProcessor(spawning_image, image_is_tiled=True)
    result = spawning_processor.run()
    if (spawning_processor.ambiguous):
      result = -1
    return result

  def get_playfield(self):
    playfield_image = self.processor.get_playfield()
    playfield_processor = PlayfieldProcessor(playfield_image, image_is_tiled=True)
    return playfield_processor.run(return_on_transition=True)

  def numbers(self, number_image):
    number_image = GameboyImage(number_image, number_image.shape[0], number_image.shape[1],
                                number_image.shape[2], number_image.shape[3], is_tiled=True)
    # number_image.untile()
    number_processor = SequentialNumberProcessor(number_image.image)
    return number_processor.get_number()

  def score(self, processor):
    score_image = processor.get_score()
    return self.numbers(score_image)

  def lines(self, processor):
    lines_image = processor.get_lines()
    return self.numbers(lines_image)

  def level(self, processor):
    level_image, heart_image = processor.get_level()
    is_heart = not Tile(heart_image[0][0]).is_white()
    return self.numbers(level_image), is_heart

  def start(self, processor):
    self.playfield_tracker.track(Playfield.empty())
    self.processor = processor
    self.playfield = self.get_playfield()

    # We want to have a clean image at the
    # start
    if (self.is_blending()):
      # Retakes an image until no blending is visible
      self.retake()

    self.saver.save(self.processor.original_image)

    self.start_score = self.score(self.processor)
    self.start_level, is_heart = self.level(self.processor)
    self.start_lines = self.lines(self.processor)

    # write current state to database
    only_one, mino = self.playfield.only_one_type_of_mino()
    if (only_one):
      self.preview_tracker.force_count(mino)
      start_preview = self.preview(self.processor)
      self.csv_file.write(self.start_score, self.start_lines, self.start_level,
                          start_preview, mino, True, self.playfield.playfield_array)

    self.state_machine()

  def is_paused(self):
    # this is a very brittle hack. We just hope
    # that not another combination of
    # minos and whites return the same result
    continue_image = self.processor.get_continue()
    break_as_number = self.numbers(continue_image)
    return (break_as_number == 471806
            or break_as_number == 871806
            or break_as_number == 11005)

  def is_over(self):
    # this is a very brittle hack. We just hope
    # that not another combination of
    # minos and whites return the same result
    please_image = self.processor.get_please()
    please_as_number = self.numbers(please_image)
    return please_as_number == 116956

  def idle(self):
    print("Game is idle")
    self.timer.start()
    while (self.is_paused() or self.is_over()) and not self.game.force_stop():
      self.timer.wait_then_restart()
      self.prepare()

  def state_machine(self):
    while (self.game.is_running(self.processor) and not self.game.force_stop()):
      if (self.is_paused() or self.is_over()):
        self.idle()
      elif (self.is_blending()):
        self.retake()
      else:
        self.run()

    self.finish()

  def finish(self):
    print(self.preview_tracker.stats)

    print("Score: " + str(self.start_score) + " to " + str(self.score_tracker.last()))
    print("Level: " + str(self.start_level) + " to " + str(self.level_tracker.last()))
    print("Lines: " + str(self.start_lines) + " to " + str(self.lines_tracker.last()))
    print("Tetris Rate: " + "{:.0%}".format(self.stats.get_tetris_rate()))

  def prepare(self):
    """
    Prepares everything for the
    next round. Resets the
    GameboyViewProcessor and the
    Playfield.
    Grabs the next image and
    makes first analysis of the
    playfield. We analyse the play
    field here because we throw everything
    away if there is blending in the
    image
    """
    # This currently needs almost three seconds...
    self.processor = self.game.get_gameboy_view_processor()
    # self.saver.save(self.processor.original_image)
    self.playfield = self.get_playfield()

  def retake(self):
    """
    Immediately retake the image if we stumbled upon
    a playfield with blending
    """
    while (self.is_blending()):
      self.prepare()

  def is_blending(self):
    """
    There is blending in the playfield
    which is too difficult to handle...
    """
    return self.playfield == None

  def run(self):
    """
    A round is in this state as long it is not
    on pause or does not have a blending playfield
    and the game is running.
    """
    self.timer.start()

    while (self.game.is_running(self.processor)
           and not self.game.force_stop()
           and not self.is_paused()
           and not self.is_blending()
           and not self.is_over()):  # Something like not processor.get_top_left_tile().is_black()
      # This uses up time. We could make it faster
      # by not saving every image but it only needs like 14 miliseconds
      # self.saver.save(self.processor.original_image)

      print("")
      score = self.score(self.processor)
      print("Raw Score: " + str(score))
      self.score_tracker.track(score)

      print("Tracked Score: " + str(self.score_tracker.last()))
      # This is only here to collect images that
      # could not get detected correctly
      # This should not happen
      if (self.score_tracker.last() == -1):
        print("stored debug image")
        cv2.imwrite("screenshots/images_to_retrain/" + str(score) + ".png",
                    GameboyImage(self.processor.get_score()).untile())

        for tile in self.processor.get_score()[0]:
          bordered = Image.fromarray(tile)
          bordered = ImageOps.expand(bordered, border=10, fill='white')
          bordered = np.array(bordered)
          self.saver.save(bordered)

      self.lines_tracker.track(self.lines(self.processor))
      self.level_tracker.track(*self.level(self.processor))
      self.playfield_tracker.track(self.playfield)
      self.preview_tracker.track(self.preview(self.processor), self.playfield_tracker)

      # calculate statistics
      clean_playfield = self.playfield_tracker.clean_playfield()
      self.stats.calculate(self.lines_tracker, self.score_tracker, self.level_tracker)
      print("Tetris Rate: " + "{:.0%}".format(self.stats.get_tetris_rate()))
      if (not np.isnan(np.array(clean_playfield, dtype=float)).any()):
        print("Paritiy: " + str(Playfield(clean_playfield).parity()))

      self.plotter.show_plot(self.score_tracker.array, self.lines_tracker.array, self.preview_tracker.stats)

      self.csv_file.write(self.score_tracker.last(), self.lines_tracker.last(), self.level_tracker.last(),
                          self.preview_tracker.last(), self.preview_tracker.spawned_piece,
                          self.preview_tracker.tetromino_spawned, self.playfield_tracker.current.playfield_array)

      self.timer.wait_then_restart()

      self.prepare()
