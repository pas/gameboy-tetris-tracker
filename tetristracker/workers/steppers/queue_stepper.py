from tetristracker.workers.get.get import Get
from tetristracker.workers.steppers.stepper import Stepper


class QueueStepper(Stepper):
  """
  Retrieves values from Getter by calling its get()
  function in each step and puts the values into
  the given queue.
  """
  def __init__(self, queue, getter: Get):
    self.queue = queue
    self.getter = getter

  def step(self):
    self.queue.put(self.getter.get())