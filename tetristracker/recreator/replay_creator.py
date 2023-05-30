from tetristracker.tile.tile_recognizer import TileRecognizer


class ReplayCreator():
  def __init__(self, round, start_index):
    self.round = round
    self.start_index = start_index

  def save(self, path):
    pieces = self._collect_pieces()
    return pieces

  def _collect_pieces(self):
    index = self.start_index
    pieces = []
    while len(pieces) < 30 and index < len(self.round):
      data = self.round[index]
      if(data[7]):
        pieces.append(data[6])
      index += 1

    pieces = self._fill(pieces)
    return pieces

  def _fill(self, pieces):
    if(len(pieces) < 30):
      for _ in range(len(pieces), 30):
        pieces.append(TileRecognizer.J_MINO)
    return pieces
