import time

from csvfile import CSVWriter
from gameboy_image import GameboyImage
from gameboy_view_processor import GameboyViewProcessor
from image_saver import ImageSaver
from number_processor import NumberProcessor
from playfield_processor import Playfield, PlayfieldProcessor
from preview_processor import SpawningProcessor, PreviewProcessor
from score_tracker import ScoreTracker, LinesTracker, LevelTracker, PreviewTracker, PlayfieldTracker


class Game:
  MIN_WAIT_TIME = 50
  def __init__(self, capturer):
    self.round = None
    self.capturer = capturer

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
    return tile.is_black()

  def get_gameboy_view_processor(self):
    image = self.capturer.grab_image()
    return GameboyViewProcessor(image)

  def state_machine(self):
    while True:
      if(self.is_running(self.processor)):
        self.run()
      else:
        self.idle()

  def run(self):
    saver = ImageSaver("test/debug/", "running")
    self.round = Round(self, saver)
    self.round.start(self.processor)
    self.processor = self.get_gameboy_view_processor()

  def start(self):
    self.processor = self.get_gameboy_view_processor()
    self.state_machine()

  def idle(self):
    """
    During idle stat we are regularly checking if
    another round has started. As soon as this is
    the case change state
    :return:
    """
    start_time = time.time() * 1000
    while not self.is_running(self.processor):
      self.processor = self.get_gameboy_view_processor()
      time_passed = time.time() * 1000 - start_time
      if (time_passed < 50):
        time.sleep((50 - time_passed) / 1000)
      start_time = time.time() * 1000

class Round:
  def __init__(self, game, saver):
    self.csv_file = CSVWriter()
    self.score_tracker = ScoreTracker()
    self.lines_tracker = LinesTracker()
    self.level_tracker = LevelTracker()
    self.preview_tracker = PreviewTracker()
    self.playfield_tracker = PlayfieldTracker()
    self.saver = saver
    self.game = game

  def preview(self, processor):
    """
    Returns -1 if results are ambigous
    """
    preview_image = processor.get_preview()
    preview_processor = PreviewProcessor(preview_image, image_is_tiled=True)
    result = preview_processor.run()
    if(preview_processor.ambigous):
      result = -1
    return result

  def spawning(self, processor):
    spawning_image = processor.get_spawning_area()
    spawning_processor = SpawningProcessor(spawning_image, image_is_tiled=True)
    result = spawning_processor.run()
    if(spawning_processor.ambigous):
      result = -1
    return result

  def get_playfield(self):
    playfield_image = self.processor.get_playfield()
    playfield_processor = PlayfieldProcessor(playfield_image, image_is_tiled=True)
    return playfield_processor.run(return_on_transition=True)

  def numbers(self, number_image):
    number_image = GameboyImage(number_image, number_image.shape[0], number_image.shape[1],
                               number_image.shape[2], number_image.shape[3], is_tiled=True)
    number_image.untile()
    number_processor = NumberProcessor(number_image.image)
    return number_processor.get_number()

  def score(self, processor):
    score_image = processor.get_score()
    return self.numbers(score_image)

  def lines(self, processor):
    lines_image = processor.get_lines()
    return self.numbers(lines_image)

  def level(self, processor):
    level_image = processor.get_level()
    return self.numbers(level_image)

  def start(self, processor):
    self.playfield_tracker.track(Playfield.empty())
    self.processor = processor
    self.playfield = self.get_playfield()
    self.saver.save(self.processor.original_image)
    self.state_machine()

  def is_paused(self):
    # this is a brittle hack. We just hope
    # that not another combination of
    # minos and whites return the same result
    continue_image = self.processor.get_continue()
    break_as_number = self.numbers(continue_image)
    return break_as_number == 571406

  def pause(self):
    while self.is_paused():
      start_time = time.time() * 1000
      self.processor = self.game.get_gameboy_view_processor()

      time_passed = time.time() * 1000 - start_time
      if (time_passed < 50):
        time.sleep((50 - time_passed) / 1000)

  def state_machine(self):
    while(self.game.is_running(self.processor)):
      if(self.is_paused()):
        print("PAUSE")
        self.pause()
      elif(self.is_blending()):
        print("RETAKE")
        self.retake()
      else:
        print("RUN")
        self.run()
    print("END")

  def retake(self):
    """
    Immediately retake the image if we stumbled upon
    a playfield with blending
    """
    while(self.is_blending()):
      self.processor = self.game.get_gameboy_view_processor()
      self.playfield = self.get_playfield()

  def is_blending(self):
    """
    There is blending in the  playfield
    which is too difficult to handle...
    """
    return self.playfield == None

  def run(self):
    """
    A round is in this state as long it is not
    on pause or does not have a blending playfield
    and the game is running.
    """
    start_time = time.time() * 1000
    while self.game.is_running(self.processor) and not self.is_paused() and not self.is_blending():  # Something like not processor.get_top_left_tile().is_black()
      # This uses up time. We could make it faster
      # by not saving every image
      self.saver.save(self.processor.original_image)

      self.score_tracker.track(self.score(self.processor))
      self.lines_tracker.track(self.lines(self.processor))
      self.preview_tracker.track(self.preview(self.processor))
      self.level_tracker.track(self.level(self.processor))

      #print("Score: " + str(self.score_tracker.last()) + " Lines: " + str(self.lines_tracker.last()))

      self.csv_file.write(self.score_tracker.last(), self.lines_tracker.last(), self.level_tracker.last(),
                          self.preview_tracker.last(), self.playfield_tracker.current.playfield_array)

      time_passed = time.time()*1000-start_time
      #print("Used time for one round: " + str(time_passed))
      if(time_passed < 50):
        time.sleep((50-time_passed)/1000)

      start_time = time.time() * 1000
      self.processor = self.game.get_gameboy_view_processor()