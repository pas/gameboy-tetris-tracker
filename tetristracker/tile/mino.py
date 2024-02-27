class Mino:
  """
  Mino are ordered in the way they appear in the
  OAM
  """
  names = ["J-mino", "Z-mino", "O-mino", "L-mino", "T-mino", "S-mino",
           "I-top-vertical-mino", "I-center-vertical-mino", "I-bottom-vertical-mino",
           "I-left-horizontal-mino", "I-center-horizontal-mino", "I-right-horizontal-mino",
           "border left", "border bottom", "border right", "border top"]
  short_name_to_number_dict = {
    "J" : 0,
    "Z" : 1,
    "O" : 2,
    "L" : 3,
    "T" : 4,
    "S" : 5,
    "I" : 6
  }
  number_to_short_name_array = [ "J", "Z", "O", "L", "T", "S", "I"]