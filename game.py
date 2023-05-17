import time

import cv2
import numpy as np
from PIL import ImageOps
from PIL import Image

from csvfile import CSVWriter
from gameboy_image import GameboyImage
from gameboy_view_processor import GameboyViewProcessor
from image_saver import ImageSaver
from number_processor import NumberProcessor, SequentialNumberProcessor
from playfield_processor import Playfield, PlayfieldProcessor
from preview_processor import SpawningProcessor, PreviewProcessor
from score_tracker import ScoreTracker, LinesTracker, LevelTracker, PreviewTracker, PlayfieldTracker
from timer import Timer


class Game:
  MIN_WAIT_TIME = 50
  def __init__(self, capturer, plotter):
    self.round = None
    self.capturer = capturer
    self.timer = Timer()
    self.plotter = plotter

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
    self.round = Round(self, saver, self.plotter)
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
    self.timer.start()
    while not self.is_running(self.processor):
      self.processor = self.get_gameboy_view_processor()
      self.timer.wait_then_restart()

class Round:
  def __init__(self, game, saver, plotter):
    self.csv_file = CSVWriter()
    self.score_tracker = ScoreTracker()
    self.lines_tracker = LinesTracker()
    self.level_tracker = LevelTracker()
    self.preview_tracker = PreviewTracker()
    self.playfield_tracker = PlayfieldTracker()
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
    #number_image.untile()
    number_processor = SequentialNumberProcessor(number_image.image)
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
    #self.saver.save(self.processor.original_image)
    self.state_machine()

  def is_paused(self):
    # this is a brittle hack. We just hope
    # that not another combination of
    # minos and whites return the same result
    continue_image = self.processor.get_continue()
    break_as_number = self.numbers(continue_image)
    return break_as_number == 571406

  def pause(self):
    self.timer.start()
    while self.is_paused():
      self.timer.wait_then_restart()
      self.prepare()

  def state_machine(self):
    while(self.game.is_running(self.processor)):
      if(self.is_paused()):
        #print("PAUSE")
        self.pause()
      elif(self.is_blending()):
        #print("RETAKE")
        self.retake()
      else:
        #print("RUN")
        self.run()

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
    self.processor = self.game.get_gameboy_view_processor()
    self.playfield = self.get_playfield()

  def retake(self):
    """
    Immediately retake the image if we stumbled upon
    a playfield with blending
    """
    while(self.is_blending()):
      self.prepare()

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
    self.timer.start()
    while self.game.is_running(self.processor) and not self.is_paused() and not self.is_blending():  # Something like not processor.get_top_left_tile().is_black()
      # This uses up time. We could make it faster
      # by not saving every image
      self.saver.save(self.processor.original_image)

      score = self.score(self.processor)
      self.score_tracker.track(score)
      #bordered = Image.fromarray(self.processor.get_score()[0][5])
      #bordered = ImageOps.expand(bordered, border=10, fill='white')
      #bordered = np.array(bordered)
      #self.saver.save(bordered)

      print("Score: " + str(self.score_tracker.last()))
      # This is only here to collect images that
      # could not get detected correctly
      if(self.score_tracker.last() == -1):
        print("stored debug image")
        cv2.imwrite("tetris/images_to_retrain/"+str(score)+".png", GameboyImage(self.processor.get_score()).untile())

      self.lines_tracker.track(self.lines(self.processor))
      self.preview_tracker.track(self.preview(self.processor))
      self.level_tracker.track(self.level(self.processor))
      self.playfield_tracker.track(self.playfield)

      #calculate statistics
      clean_playfield = self.playfield_tracker.clean_playfield()
      #if(not np.isnan(np.array(clean_playfield, dtype=np.float)).any()):
        #print(Playfield(clean_playfield).parity())

      self.plotter.show_plot(self.score_tracker.array, self.lines_tracker.array)
      self.csv_file.write(self.score_tracker.last(), self.lines_tracker.last(), self.level_tracker.last(),
                          self.preview_tracker.last(), self.playfield_tracker.current.playfield_array)

      self.timer.wait_then_restart()
      self.prepare()