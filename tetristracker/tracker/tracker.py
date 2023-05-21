class Tracker:
  """
  Only tracks ints
  """
  def __init__(self):
    self.accepted = -1
    self.array = []

  def track(self, value):
    """
    A None value gets tracked as -1
    but does not update the
    accepted_score value
    """
    if (value != None):
      self.accepted = value
      self.array.append(int(value))
    else:
      self.array.append(-1)

  def is_accepted(self):
    return not self.array[len(self.array) - 1] == -1

  def is_empty(self):
    return len(self.array) == 0

  def last(self):
    """
    Returns always None if there is no value stored
    """
    if(len(self.array) > 0):
      return self.array[len(self.array) - 1]
    else:
      return None

  def has_changed(self):
    """
    Returns always false if there is only one value stored.
    """
    if(len(self.array) > 1):
      return self.array[len(self.array)-1] != self.array[len(self.array)-2]
    else:
      return False
