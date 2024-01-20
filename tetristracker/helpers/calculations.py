import numpy as np

def get_slope(X, Y):
  """
  By kimstik
  From https://stackoverflow.com/a/58032878
  """
  return np.polyfit(X, Y, 1)[0]


def number_to_hex_string(number):
  return f'{number:02x}'.upper()

def number_to_image_path(number):
  hex_number = number_to_hex_string(number)
  return "images/tiles/" + hex_number + ".png"

def tile_number_to_image_number(tile_nr):
  array = [0x81, 0x82, 0x83, 0x84, 0x85, 0x86, 0x80, 0x88, 0x89, 0x8A, 0x8B, 0x8F]
  if(tile_nr == -99):
    return 47

  return array[tile_nr]