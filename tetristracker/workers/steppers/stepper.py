from abc import abstractmethod


class Stepper:
  """
  Interface to implement a Object
  that steps through something intend
  to be used as a step in a inifinite
  loop (see Looper)
  """
  @abstractmethod
  def step(self):
   pass