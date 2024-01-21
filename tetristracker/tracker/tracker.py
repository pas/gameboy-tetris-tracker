class Tracker:
  """
  Only tracks ints
  """
  def __init__(self):
    self.accepted = None
    self.array = []

  def track(self, value):
    """
    A None value gets tracked as -1
    but does not update the
    accept value

    Accepts only positive numbers
    and 0. None gets translated to -1.

    Don't pass -1 as value!
    """
    assert(value != -1)
    if (value != None):
      self.accepted = value
      self.array.append(int(value))
    else:
      self.array.append(-1)

  def is_accepted(self):
    """
    Returns true if last tracked
    item got accepted by
    the tracker.

    Sidenote: Accepted means that
    the passed value got stored. If
    a value is not accepted then
    the value -1 gets stored
    instead of the passed value

    This method is undefined if no values
    are tracked

    :return: True if last item got accepted. False otherwise.
    """
    assert(not self.is_empty())

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
    Compares the last two inserted values. Asserts
    true if both values are different and false
    otherwise.
    Currently, no intelligent tackling of -1
    values...
    Returns always false if there is only one value stored.
    """
    if(len(self.array) > 1):
      return self.array[len(self.array)-1] != self.array[len(self.array)-2]
    else:
      return False
