from tetristracker.capturer.capture_selection import CaptureSelection
from tetristracker.helpers.config import Config
from tetristracker.plotter.plotter_selection import PlotterSelection
from tetristracker.storage.storage_selection import StorageSelection
from tetristracker.workers.get.gameboy_view_processor_to_playfield_processor import GameboyViewProcessorToPlayfieldProcessor
from tetristracker.workers.get.image_capture import ImageCapture
from tetristracker.workers.get.image_to_gameboy_view_processor import ImageToGameboyViewProcessor
from tetristracker.workers.steppers.multiple_queues_stepper import MultipleQueuesSequentialStepper
from tetristracker.workers.steppers.queue_stepper import QueueStepper
from tetristracker.workers.steppers.stepper import Stepper
from tetristracker.workers.steppers.store_and_plot_stepper import StoreAndPlotStepper


class Looper():
  """
  Starts an infinite loop that calls #step
  the passed Stepper in each loop.
  """
  def __init__(self, stepper: Stepper):
    self.stepper = stepper

  def start(self):
    while True:
      self.stepper.step()

def _start_loop(stepper : Stepper):
  looper = Looper(stepper)
  looper.start()

def capture(images_queue):
  """
  Capturing images and put them into the
  queue
  """
  print("capture")

  # create capturer (this seems to have to be inside
  # the local thread or else mss doesn't work)
  config = Config()
  capture_selection = CaptureSelection(config)
  capture_selection.select(config.get_capturer())

  getter = ImageCapture(capture_selection.get())
  stepper = QueueStepper(images_queue, getter)
  _start_loop(stepper)

def prepare_gameboy_view(shift_score, images_queue, playfield_image_queues):
  """
  Prepares the captured images inside the queue.
  Put result into queue.
  """
  print("gb view")
  getter = ImageToGameboyViewProcessor(shift_score, images_queue)
  stepper = MultipleQueuesSequentialStepper(playfield_image_queues, getter)
  _start_loop(stepper)


def prepare_playfield(playfield_image_queues, playfield_queue):
  """
  Prepares the playfield.
  Put results into queue
  """
  print("playfield")
  getter = GameboyViewProcessorToPlayfieldProcessor(playfield_image_queues)
  stepper = QueueStepper(playfield_queue, getter)
  _start_loop(stepper)

def store_and_plot(result_queue):
  print("store and plot")
  config = Config()
  # The objects for plotter and storage need to be created
  # inside this process...
  storage_selection = StorageSelection()
  storage_selection.select(config.get_storage())
  plotter_selection = PlotterSelection()
  plotter_selection.select(config.get_plotter())
  storage = storage_selection.get()
  plotter = plotter_selection.get()

  stepper = StoreAndPlotStepper(result_queue, storage, plotter)
  _start_loop(stepper)
