import numpy as np

from tetristracker.commasv.sqlite_reader import SqliteReader
from tetristracker.helpers.calculations import number_to_hex_string, tile_number_to_image_number
from tetristracker.tile.tetromino_transmission import MinoToTetrominoConverter, TetrominoTransmission


class ReplayCreator():
  MAX_PIECES = 256
  def __init__(self, round_value, start_index):
    self.set(round_value, start_index)
    self.converter = MinoToTetrominoConverter()

  def create(self):
    pieces_string = self._collect_pieces()
    garbage_string = self._create_garbage()
    return { "pieces" : pieces_string,
             "garbage" : garbage_string }

  def set_start_index(self, start_index):
    self.start_index = start_index

  def set_round(self, round_value):
    self.round = round_value

  def set(self, round_value, start_index):
    self.set_start_index(start_index)
    # index must be set before round!
    self.set_round(round_value)

  def _create_garbage(self):
    # only select the part that can be injected into the B-Type
    playfield_array = self.round[self.start_index][SqliteReader.PLAYFIELD]
    garbage = np.array(playfield_array[8:19]).flatten()
    garbage = self._map_to_mino_image_nr(garbage)
    garbage_string = self._concatenate(garbage)
    return garbage_string

  def _map_to_mino_image_nr(self, minos):
    transmissible_minos = []
    for mino in minos:
      transmissible_minos.append(tile_number_to_image_number(mino))
    return transmissible_minos


  def _collect_pieces(self):
    index = self.start_index
    pieces = []

    # Set first piece
    if not self.round[index][SqliteReader.SPAWNED]:
      pieces.append(self.round[index][SqliteReader.TETROMINO_IN_PLAY])

    while len(pieces) < self.MAX_PIECES and index < len(self.round):
      data = self.round[index]
      if(data[SqliteReader.SPAWNED]):
        pieces.append(data[SqliteReader.TETROMINO_IN_PLAY])
      index += 1

    pieces = self._map_to_tetromino(pieces)
    pieces = self._fill(pieces)
    pieces_string = self._concatenate(pieces)

    return pieces_string

  def _concatenate(self, pieces):
    string = ""
    for piece in pieces:
      string += number_to_hex_string(piece)
    return string

  def _fill(self, pieces):
    if(len(pieces) < self.MAX_PIECES):
      for _ in range(len(pieces), self.MAX_PIECES):
        pieces.append(TetrominoTransmission.L_TETROMINO)
    return pieces

  def _map_to_tetromino(self, pieces):
    transmissible_pieces = []
    for piece in pieces:
      transmissible_pieces.append(self.converter.convert(piece))
    return transmissible_pieces

