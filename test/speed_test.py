import multiprocessing
import time
import unittest
from multiprocessing import Process
from queue import Queue
from threading import Thread

from test.helpers import get_image
from tetristracker.capturer.image_sequence_capturer import ImageSequenceCapturer
from tetristracker.capturer.mss_capturer import MSSCapturer
from tetristracker.commasv.writer import Writer
from tetristracker.game import Game, Round
from tetristracker.helpers.config import Config
from tetristracker.image.gameboy_image import GameboyImage
from tetristracker.processor.gameboy_view_processor import GameboyViewProcessor
from tetristracker.processor.number_processor import SimplisticSequentialNumberProcessor, SequentialNumberProcessor, \
  NumberProcessor
from tetristracker.processor.playfield_processor import PlayfieldProcessor
from tetristracker.runner import Runner
from tetristracker.tile.tile import Tile
from tetristracker.tile.tile_recognizer import TileRecognizer

q_1 = Queue()
q_2 = Queue()
q_3 = Queue()
m_q = [q_2, q_3]

m_p_q = multiprocessing.JoinableQueue()

m_p_q_1 = multiprocessing.JoinableQueue()
m_p_q_2 = multiprocessing.JoinableQueue()
m_p_q_3 = multiprocessing.JoinableQueue()
m_p_q_4 = multiprocessing.JoinableQueue()
m_m_p_q = [m_p_q_1, m_p_q_2, m_p_q_3, m_p_q_4]

def worker():
  while True:
    image = q_1.get()
    processor = GameboyViewProcessor(image)
    q_1.task_done()

def worker1():
  while True:
    image = q_1.get()
    processor = GameboyViewProcessor(image)
    q_2.put(processor.get_playfield())
    q_1.task_done()

def workerMultiQueues():
  current = 0
  while True:
    image = q_1.get()
    processor = GameboyViewProcessor(image)
    selected_queue = m_q[current]
    selected_queue.put(processor.get_playfield())
    current = (current+1) % 2
    q_1.task_done()

def worker_multi_process_1():
  while True:
    image = q_1.get()
    processor = GameboyViewProcessor(image)
    m_p_q.put(processor.get_playfield())
    q_1.task_done()

def worker_multi_process_2(m_p_q : multiprocessing.JoinableQueue):
  while True:
    image = m_p_q.get()
    processor = PlayfieldProcessor(image, image_is_tiled=True)
    processor.run()
    m_p_q.task_done()

def worker2():
  while True:
    image = q_2.get()
    processor = PlayfieldProcessor(image, image_is_tiled=True)
    processor.run()
    q_2.task_done()

def worker3():
  while True:
    image = q_3.get()
    processor = PlayfieldProcessor(image, image_is_tiled=True)
    processor.run()
    q_3.task_done()

class TestSpeed(unittest.TestCase):
  def setUp(self):
    with q_1.mutex:
      q_1.queue.clear()
    with q_2.mutex:
      q_2.queue.clear()
    with q_3.mutex:
      q_3.queue.clear()
    m_p_q = multiprocessing.JoinableQueue()
    m_p_q_1 = multiprocessing.JoinableQueue()
    m_p_q_2 = multiprocessing.JoinableQueue()
    m_p_q_3 = multiprocessing.JoinableQueue()
    m_p_q_4 = multiprocessing.JoinableQueue()
    m_m_p_q = [m_p_q_1, m_p_q_2, m_p_q_3, m_p_q_4]


  def get_mss_capturer(self):
    config = Config()
    return MSSCapturer(config.get_screen_bounding_box())

  """
  Trying to optimize speed:
  Goal: at least 30 images per second
  """
  def test_mss_speed(self):
    """
    This seems to be fine. Around 59 images per second
    can get captured.
    :return:
    """
    mssCapturer = self.get_mss_capturer()

    iterations = 120 # 4 seconds

    start = time.perf_counter()
    for _ in range(0, iterations):
      mssCapturer.grab_image()
    end = time.perf_counter()
    passed_time = end-start
    print("Needed " + str(passed_time) + " seconds for " + str(iterations) + " images.")
    print(str(iterations / passed_time) + " images for 1 second")

    # Measured on 19-02-2024: 2.03, 2.17, 2.03, 2.18, 2.04
    self.assertTrue(passed_time < 2.2)

  def test_mss_speed_with_gv_processor(self):
    """
    This seems to be fine. Around 37 images per second
    can get captured.

    We don't need to worry what the mss capturer returns
    as the only thing we do in GameboyViewProcessor
    is resize the image (see GameboyViewProcessor#_tile_image)
    """
    mss_capturer = self.get_mss_capturer()

    iterations = 120  # 4 seconds

    start = time.perf_counter()
    for _ in range(0, iterations):
      image = mss_capturer.grab_image()
      gv_processor = GameboyViewProcessor(image)

    end = time.perf_counter()
    passed_time = end - start
    print("Needed " + str(passed_time) + " seconds for " + str(iterations) + " images.")
    print(str(iterations / passed_time) + " images for 1 second")

    # Measured on 19-02-2024: 3.3, 3.2, 3.4, 3.5, 3.5, 3.2
    self.assertTrue(passed_time < 3.6)

  def test_mss_speed_with_gv_processor_with_queues(self):
    """
    This is more or less how it is implemented
    in game. Cannot test it separately so
    we mimick the behaviour. This might
    be completely wrong...

    TODO: I think this means that we can move this and the previous
    TODO: action into one process and using Threads there.
    """
    t = Thread(target=worker, daemon=True)
    t.start()

    mss_capturer = self.get_mss_capturer()

    iterations = 120  # 4 seconds

    start = time.perf_counter()
    for _ in range(0, iterations):
      image = mss_capturer.grab_image()
      q_1.put(image)

    q_1.join()

    end = time.perf_counter()
    passed_time = end - start

    # This is even slightly faster than the non-threaded one
    print("Needed " + str(passed_time) + " seconds for " + str(iterations) + " images.")
    print(str(iterations / passed_time) + " images for 1 second")

    # Measured on 19-02-2024: 2.03, 2.03, 2.01, 2.02
    self.assertTrue(passed_time < 2.1)

  def test_mss_speed_with_gv_processor_and_playfield_processor(self):
    """
    This is all without threading
    to see the difference.
    The problem here is that we do work
    in Playfield processor, so we use
    the image grabbed through the
    GameboyViewProcessor (where before
    we only did resize the image).
    This means this is dependend
    on the input image... This makes
    this a very brittle test...

    This should be quite slow.
    """
    mss_capturer = self.get_mss_capturer()

    iterations = 120  # 4 seconds

    start = time.perf_counter()
    for _ in range(0, iterations):
      image = mss_capturer.grab_image()
      gv_processor = GameboyViewProcessor(image)
      processor = PlayfieldProcessor(gv_processor.get_playfield(), image_is_tiled=True)
      processor.run()

    end = time.perf_counter()
    passed_time = end - start

    print("Needed " + str(passed_time) + " seconds for " + str(iterations) + " images.")
    print(str(iterations / passed_time) + " images for 1 second")

    # 10.0, 9.8, 10.1, 10.1
    self.assertTrue(passed_time < 10.2)

  def test_mss_speed_with_gv_processor_and_playfield_processor_with_queues(self):
    """
    This is more or less how it is implemented
    in game. Cannot test it separately so
    we mimick the behaviour. This might
    be completely wrong...

    Through this it is possible to win around 7 more images per second
    (see #test_mss_speed_with_gv_processor_and_playfield_processor)
    """
    t1 = Thread(target=worker1, daemon=True)
    t2 = Thread(target=worker2, daemon=True)
    t1.start()
    t2.start()

    mss_capturer = self.get_mss_capturer()

    iterations = 120  # 4 seconds

    start = time.perf_counter()
    for _ in range(0, iterations):
      image = mss_capturer.grab_image()
      q_1.put(image)

    q_1.join()
    q_2.join()

    end = time.perf_counter()
    passed_time = end - start

    print("Needed " + str(passed_time) + " seconds for " + str(iterations) + " images.")
    print(str(iterations / passed_time) + " images for 1 second")

    # Measured 19-02-2024: 6.7, 6.5, 6.6, 6.4, 6.4
    self.assertTrue(passed_time < 6.8)

  def test_mss_speed_with_gv_processor_and_playfield_processor_with_queues_multiprocessed(self):
    """
    This is more or less how it is implemented
    in game. Cannot test it separately so
    we mimick the behaviour. This might
    be completely wrong...

    Through this it is possible to win around 7 more images per second
    (see #test_mss_speed_with_gv_processor_and_playfield_processor)

    This is around the same gain as using Threads. So now win here
    with multiprocessing. :(
    """
    t1 = Thread(target=worker_multi_process_1, daemon=True)
    t2 = Process(target=worker_multi_process_2, args=(m_p_q,), daemon=True)
    t1.start()
    t2.start()

    mss_capturer = self.get_mss_capturer()

    iterations = 120  # 4 seconds

    start = time.perf_counter()
    for _ in range(0, iterations):
      image = mss_capturer.grab_image()
      q_1.put(image)

    q_1.join()
    m_p_q.join()

    end = time.perf_counter()
    passed_time = end - start

    print("Needed " + str(passed_time) + " seconds for " + str(iterations) + " images.")
    print(str(iterations / passed_time) + " images for 1 second")

    # Measured 19-02-2024: 6.7, 6.5, 6.6, 6.4, 6.4
    self.assertTrue(passed_time < 6.8)

  def test_mss_speed_with_gv_processor_and_playfield_processor_with_multi_queues(self):
    """
    This is more or less how it is implemented
    in game. Cannot test it separately so
    we mimick the behaviour. This might
    be completely wrong...

    Multiple queues in threading does not make anything faster here...
    it even slows everything down

    Through this it is possible to win around 7 more images per second
    (see #test_mss_speed_with_gv_processor_and_playfield_processor)
    """
    t1 = Thread(target=workerMultiQueues, daemon=True)
    t2 = Thread(target=worker2, daemon=True)
    t3 = Thread(target=worker3, daemon=True)
    t1.start()
    t2.start()
    t3.start()

    mss_capturer = self.get_mss_capturer()

    iterations = 120  # 4 seconds

    start = time.perf_counter()
    for _ in range(0, iterations):
      image = mss_capturer.grab_image()
      q_1.put(image)

    q_1.join()
    q_2.join()
    q_3.join()

    end = time.perf_counter()
    passed_time = end - start

    print("Needed " + str(passed_time) + " seconds for " + str(iterations) + " images.")
    print(str(iterations / passed_time) + " images for 1 second")

    # Measured 19-02-2024: 8.1, 8.0, 7.9, 8.2
    self.assertTrue(passed_time < 8.3)

  class GameMock():
    def __init__(self, images: Queue, playfield_processors: Queue):
      self.images = images
      self.playfield_processors = playfield_processors

    def get_gameboy_view_processor(self):
      return self.images.get(), self.playfield_processors.get()

    def is_running(self, processor):
      return not self.images.empty()

    def force_stop(self):
      return False

  class MockPlotter:
    def show_plot(self, x, y, z):
      pass

  class MockWriter(Writer):
    def write(self, score: int, lines: int, level: int, preview: int, tetromino_in_play: int, spawned: bool, playfield):
      pass

    def restart(self):
      pass

  class MockSaver():
    def save(self, processor):
      pass

  class MockTracker():
    def __init__(self):
      self.array = []
      self.stats = None
      self.spawned_piece = None
      self.tetromino_spawned = None
      self.current = self
      self.playfield_array = None

    def track(self, *args):
      pass

    def last(self):
      return 1

    def is_accepted(self):
      return True

    def difference(self):
      return 40

    def reject(self):
      pass

    def force_count(self, x):
      pass

    def clean_playfield(self):
      return None

  def test_run_speed(self):
    iterations = 120
    capturer = ImageSequenceCapturer("test/sequence/full-game-with-transition/retrieved",
                                     nr_of_images=iterations,
                                     start_nr=52)

    gameboy_view_processors = Queue()
    playfield_processors = Queue()
    while(capturer.has_image()):
      processor = GameboyViewProcessor(image=capturer.grab_image(), counter=1)
      gameboy_view_processors.put(processor)
      playfield = PlayfieldProcessor(processor.get_playfield(), image_is_tiled=True).run()
      playfield_processors.put(playfield)

    game = TestSpeed.GameMock(gameboy_view_processors, playfield_processors)
    writer = TestSpeed.MockWriter()
    plotter = TestSpeed.MockPlotter()
    saver = TestSpeed.MockSaver()

    start = time.perf_counter()
    round = Round(game, saver, plotter, writer)
    processor = gameboy_view_processors.get()
    playfield = playfield_processors.get()

    # Replace tracker
    #round.score_tracker = TestSpeed.MockTracker()
    #round.preview_tracker = TestSpeed.MockTracker()
    #round.playfield_tracker = TestSpeed.MockTracker()
    #round.numbers = self.mock_numbers

    round.start(processor, playfield)
    end = time.perf_counter()

    passed_time = end - start
    print("Needed " + str(passed_time) + " seconds for " + str(iterations) + " images.")
    print(str(iterations/passed_time) + " images for 1 second")
    self.assertTrue(passed_time < 4.0)

  def mock_numbers(self, x):
    return 4

  def get_tiled_image(self, path, number_of_tiles_height, number_of_tiles_width, tile_height, tile_width):
    image = get_image(path)
    gb_image = GameboyImage(image, number_of_tiles_height, number_of_tiles_width, tile_height, tile_width, is_tiled=False)
    return gb_image.tile()

  def test_simplistic_vs_sequential_vs_standard_number_processor(self):
    iterations = 100

    image = self.get_tiled_image("test/numbers/12097.png", 1, 6, 48, 48)

    start = time.perf_counter()
    for _ in range(0, iterations):
      processor = SimplisticSequentialNumberProcessor(image)
      result = processor.get_number()
    end = time.perf_counter()

    passed_time_simple = end - start

    print("passed time simplistic sequential: " + str(passed_time_simple))

    start = time.perf_counter()
    for _ in range(0, iterations):
      processor = SequentialNumberProcessor(image)
      result = processor.get_number()
    end = time.perf_counter()

    passed_time_seq = end - start

    print("passed time sequential: " + str(passed_time_seq))

    image = get_image("test/numbers/12097.png")
    start = time.perf_counter()
    for _ in range(0, iterations):
      processor = NumberProcessor(image)
      result = processor.get_number()
    end = time.perf_counter()

    passed_time_standard = end - start

    print("passed time standard: " + str(passed_time_standard))

  def test_playfield_processing_speed(self):
    """
    This is the offending part which is very
    slow. I'd like to have this at a
    way higher speed.
    Currently, at 15 images per second
    Goal: 30 images per second
    :return:
    """
    iterations = 60
    start_nr = 143
    capturer = ImageSequenceCapturer("test/sequence/full-game-with-transition/retrieved",
                                     nr_of_images=iterations,
                                     start_nr=start_nr)

    images = Queue()
    while (capturer.has_image()):
      images.put(GameboyViewProcessor(image=capturer.grab_image(), counter=0))

    start = time.perf_counter()
    for _ in range(0, iterations):
      processor = images.get()
      playfield_image = processor.get_playfield()
      playfield_processor = PlayfieldProcessor(playfield_image, image_is_tiled=True)
      playfield_processor.run(return_on_transition=False)

    end = time.perf_counter()

    passed_time = end - start
    print("Needed " + str(passed_time) + " seconds for " + str(iterations) + " images.")
    print(str(iterations / passed_time) + " images for 1 second")
    self.assertTrue(passed_time < 2.0)

  def test_playfield_processing_speed_with_processes(self):
    """
    Using 4 process to run.
    Can run around 58 images this way
    which is fast enough
    """
    t1 = Process(target=worker_multi_process_2, args=(m_p_q_1,), daemon=True)
    t2 = Process(target=worker_multi_process_2, args=(m_p_q_2,), daemon=True)
    t3 = Process(target=worker_multi_process_2, args=(m_p_q_3,), daemon=True)
    t4 = Process(target=worker_multi_process_2, args=(m_p_q_4,), daemon=True)
    t1.start()
    t2.start()
    t3.start()
    t4.start()

    iterations = 120
    start_nr = 143
    capturer = ImageSequenceCapturer("test/sequence/full-game-with-transition/retrieved",
                                     nr_of_images=iterations,
                                     start_nr=start_nr)

    images = Queue()
    while (capturer.has_image()):
      images.put(GameboyViewProcessor(image=capturer.grab_image(), counter=0).get_playfield())

    start = time.perf_counter()
    current = 0
    number_of_processes = 4
    for _ in range(0, iterations):
      processor = images.get()
      m_m_p_q[current].put(processor)
      current = (current + 1) % number_of_processes

    m_p_q_1.join()
    m_p_q_2.join()
    m_p_q_3.join()
    m_p_q_4.join()

    end = time.perf_counter()

    passed_time = end - start
    print("Needed " + str(passed_time) + " seconds for " + str(iterations) + " images.")
    print(str(iterations / passed_time) + " images for 1 second")

    # 19-02.2024 recorded: 2.07, 1.99, 2.01, 2.06, 2.03, 2.1, 2.2, 2.1, 2.02
    self.assertTrue(passed_time < 2.3)


  def test_tile_speed(self):
    recognizer = TileRecognizer()
    recognizer.create_mino_array()

    iterations = 10000

    start = time.perf_counter()
    for _ in range(0, iterations):
      tile = Tile(TileRecognizer.mino_array[0])
    end = time.perf_counter()

    passed_time_create = end - start


    tile = Tile(TileRecognizer.mino_array[0])

    start = time.perf_counter()
    for _ in range(0, iterations):
      tile.is_white()
    end = time.perf_counter()

    passed_time_white = end - start

    start = time.perf_counter()
    for _ in range(0, iterations):
      tile.brightness()
    end = time.perf_counter()

    passed_time_brightness = end - start

    start = time.perf_counter()
    for _ in range(0, iterations):
      tile.center_brightness()
    end = time.perf_counter()

    passed_time_center_brightness = end - start

    start = time.perf_counter()
    for _ in range(0, iterations):
      tile.is_in_transition()
    end = time.perf_counter()

    passed_time_in_transition = end - start

    start = time.perf_counter()
    for _ in range(0, iterations):
      tile.is_dull()
    end = time.perf_counter()

    passed_time_dull = end - start

    start = time.perf_counter()
    for _ in range(0, iterations):
      tile.is_black()
    end = time.perf_counter()

    passed_time_black = end - start

    start = time.perf_counter()
    for _ in range(0, iterations):
      tile.is_one_color()
    end = time.perf_counter()

    passed_time_one_color = end - start

    print("Create: " + str(passed_time_create))
    print("White: " + str(passed_time_white))
    print("Brightness: " + str(passed_time_brightness))
    print("Center brightness: " + str(passed_time_center_brightness))
    print("In transition: " + str(passed_time_in_transition))
    print("Dull: " + str(passed_time_dull))
    print("Black: " + str(passed_time_black))
    print("One color: " + str(passed_time_one_color))

