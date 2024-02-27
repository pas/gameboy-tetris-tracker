from tetristracker.workers.steppers.stepper import Stepper


class StoreAndPlotStepper(Stepper):
  def __init__(self, queue, storage, plotter):
    self.storage = storage
    self.plotter = plotter
    self.queue = queue

  def step(self):
    (plot_values, store_values) = self.queue.get()
    self.plotter.show_plot(*plot_values)
    self.storage.write(*store_values)