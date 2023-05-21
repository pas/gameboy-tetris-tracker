import numpy as np
from PIL import Image

def convert_to_4bitgrey(image):
  """
  Converts the image to a grey scale image
  only using four colors
  """
  return np.array(Image.fromarray(image).convert(mode="P", palette=Image.ADAPTIVE, colors=4))

def convert_4bitgrey_to_grey(image):
  image = image.copy()
  image[image==1] = 84
  image[image==2] = 170
  image[image==3] = 255
  print(image)
  return image

def convert_to_rgb(image):
  """
  Converts image to a rgb image
  """
  return np.array(Image.fromarray(image).convert('RGB'))

def trim(image):
  """
  Removing all black borders from the
  given image.
  """
  return _trim(image, 0, 0, 0, 0)

def _trim(frame, top, bottom, left, right):
  if frame.shape[0] == 0:
    return np.zeros((0, 0, 3))

  # crop top
  if not np.sum(frame[0]):
    return _trim(frame[1:], top + 1, bottom, left, right)
  # crop bottom
  elif not np.sum(frame[-1]):
    return _trim(frame[:-1], top, bottom + 1, left, right)
  # crop left
  elif not np.sum(frame[:, 0]):
    return _trim(frame[:, 1:], top, bottom, left + 1, right)
    # crop right
  elif not np.sum(frame[:, -1]):
    return _trim(frame[:, :-1], top, bottom, left, right + 1)

  return frame, top, bottom, left, right
