from tetristracker.workers.gameboy_view_processor_to_playfield_processor import GameboyViewProcessorToPlayfieldProcessor
from tetristracker.workers.get import Get
from tetristracker.workers.image_capture import ImageCapture
from tetristracker.workers.image_to_gameboy_view_processor import ImageToGameboyViewProcessor


def put_queue(queue, getter: Get):
  """
  Starts an infinite loop that retrieves
  values from getter by calling its get()
  function. Then puts them into the given
  queue.

  :param queue: queue where values gets put in
  :param callable: Should return values to be passed to the queue
  :return:
  """
  while (True):
    queue.put(getter.get())

def put_queues(queues : [], getter: Get):
  """
  Starts an infinite loop that retrieves
  values from getter by calling its get()
  function. Then puts them into queues
  by rotating through them. Starting with
  the queue at index 0.
  """
  select = 0
  while (True):
    queues[select].put(getter.get())
    select = (select + 1) % 4

def capture(images_queue):
  """
  Capturing images and put them into the
  queue
  """
  print("capture")
  getter = ImageCapture()
  put_queue(images_queue, getter)

def prepare_gameboy_view(shift_score, images_queue, playfield_image_queues):
  """
  Prepares the captured images inside the queue.
  Put result into queue.
  """
  print("gb view")
  getter = ImageToGameboyViewProcessor(shift_score, images_queue)
  put_queues(playfield_image_queues, getter)


def prepare_playfield(playfield_image_queues, playfield_queue):
  """
  Prepares the playfield.
  Put results into queue
  """
  print("playfield")
  getter = GameboyViewProcessorToPlayfieldProcessor(playfield_image_queues)
  put_queue(playfield_queue, getter)
