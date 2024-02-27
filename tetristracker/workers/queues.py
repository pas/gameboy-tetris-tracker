# from queue import Queue
from multiprocessing import Queue

class Queues():
  # TODO: Handle cases when queues gets overfull!
  """
    Queue where the capturer stores
    raw images
  """
  images_queue = Queue(maxsize=4)
  """
    Queue where the playfield image is stored
  """
  playfield_image_queues = [Queue(maxsize=2), Queue(maxsize=2), Queue(maxsize=2),Queue(maxsize=2)]
  """
    Queue where there Playfield object is stored
  """
  playfield_queue = Queue(maxsize=2*len(playfield_image_queues))
  """
    Queue where results and plotting data is passed to
    the next process
  """
  result_queue = Queue()
