from tetristracker.workers.get.get import Get
from tetristracker.workers.steppers.stepper import Stepper


class MultipleQueuesSequentialStepper(Stepper):
  """
  Retrieves
  values from getter by calling its get()
  function. Then puts them into queues
  by rotating through them. Starting with
  the queue at index 0.
  """
  def __init__(self, queues, getter: Get):
    self.queues = queues
    self.getter = getter
    self.select = 0

  def step(self):
    self.queues[self.select].put(self.getter.get())
    self.select = (self.select + 1) % 4