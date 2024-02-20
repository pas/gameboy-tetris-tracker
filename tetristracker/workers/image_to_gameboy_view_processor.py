from tetristracker.image.image_saver import ImageSaver
from tetristracker.processor.gameboy_view_processor import GameboyViewProcessor
from tetristracker.workers.get import Get


class ImageToGameboyViewProcessor(Get):
  def __init__(self, shift_score, images_queue):
    self.i_queue = images_queue
    self.shift_score = shift_score
    self.saver = ImageSaver("screenshots/debug/", "retrieved")
    self.counter = 0

  def get(self):
    image = self.i_queue.get()
    #self.i_queue.task_done()
    self.saver.save(image)
    # until here everything needs to be streamlined
    # if this is not the case anymore then we need to move
    # the counter out of this class
    view = GameboyViewProcessor(image, self.counter, shift_score=self.shift_score)
    self.counter += 1
    return view