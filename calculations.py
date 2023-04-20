import numpy as np

def get_slope(X, Y):
  """
  By kimstik
  From https://stackoverflow.com/a/58032878
  """
  return np.polyfit(X, Y, 1)[0]
