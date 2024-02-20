from tetristracker.processor.gameboy_view_processor import GameboyViewProcessor
from tetristracker.processor.playfield_processor import PlayfieldProcessor
from tetristracker.workers.get import Get


class GameboyViewProcessorToPlayfieldProcessor(Get):
  # this class is used in multiple threads!
  def __init__(self, queue):
    self.queue = queue

  def get(self):
    gameboyview : GameboyViewProcessor = self.queue.get()
    #self.queue.task_done()
    playfield = None
    if(gameboyview.get_top_left_tile().is_black()):
      processor = PlayfieldProcessor(gameboyview.get_playfield(), image_is_tiled=True)
      playfield = processor.run()
    return gameboyview, playfield