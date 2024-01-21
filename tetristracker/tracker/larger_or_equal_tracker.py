from tetristracker.tracker.tracker import Tracker


class LargerOrEqualTracker(Tracker):
  """
  This tracker checks if the incoming
  value is higher or equal to the last
  accepted value in the tracker.

  If this is not the case it passes None as value
  to the parent.

  Sidenote: A None value gets translated to -1
  in the parent but does not update the
  last accepted value.
  """
  def track(self, value):
    if(value != None):
      if(not self.is_empty()):
        if(value < self.accepted):
          value = None

    super().track(value)

  def _findAccepted(self, index):
    """
    Recursive method to find the last
    accepted value backward from
    the given index
    :param index of the array
    :return: the accepted value or 0
    """
    if(index < 0):
      return 0
    if(self.array[index] != -1):
      return self.array[index]
    else:
      return self._findAccepted(index-1)

  def difference(self):
    """
    Calculates difference between the last accepted
    lines and the current.

    Returns None if this is not possible
    """
    if(self.is_empty() or self.last() == -1):
      return None

    if(len(self.array) == 1 and self.last() != -1):
      return self.last()

    return self.last() - self._findAccepted(len(self.array)-2)