from tetristracker.tile.tile_recognizer import TileRecognizer


class TetrominoTransmission:
  # pieces turn clockwise
  #00 : l
  #04 : j
  #08 : i
  #0C : o
  #10 : z
  #14 : s
  #18 : t

  # l lays flat facing down
  L_TETROMINO = 0 #00
  L_TETROMINO_90 = 1
  L_TETROMINO_180 = 2
  L_TETROMINO_270 = 3
  # j lays flat facing down
  J_TETROMINO = 4 #04
  J_TETROMINO_90 = 5
  J_TETROMINO_180 = 6
  J_TETROMINO_270 = 7
  # i lays flat
  I_TETROMINO = 8 #08
  I_TETROMINO_90 = 9
  # o is just o ;)
  O_TETROMINO = 12 #0C
  # z lays flat (three pieces wide)
  Z_TETROMINO = 16 #0A
  Z_TETROMINO_90 = 17
  # s lays flat (three pieces wide)
  S_TETROMINO = 20 #0C
  S_TETROMINO_90 = 21
  # t lays flat facing down
  T_TETROMINO = 24 #14
  T_TETROMINO_90 = 25
  T_TETROMINO_180 = 26
  T_TETROMINO_270 = 27



class MinoToTetrominoConverter:
  def __init__(self):
    self.mapper = {
      TileRecognizer.L_MINO: TetrominoTransmission.L_TETROMINO,
      TileRecognizer.J_MINO: TetrominoTransmission.J_TETROMINO,
      TileRecognizer.I_MINO_SIMPLE: TetrominoTransmission.I_TETROMINO,
      TileRecognizer.Z_MINO: TetrominoTransmission.Z_TETROMINO,
      TileRecognizer.S_MINO: TetrominoTransmission.S_TETROMINO,
      TileRecognizer.T_MINO: TetrominoTransmission.T_TETROMINO,
      TileRecognizer.O_MINO: TetrominoTransmission.O_TETROMINO
    }

  def convert(self, mino):
    return self.mapper[mino]
