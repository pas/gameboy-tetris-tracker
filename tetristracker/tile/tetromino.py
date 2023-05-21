from tetristracker.tile.tetromino_transmission import TetrominoTransmission


class Tetromino:
  @staticmethod
  def get_surface_array_l1():
    return [[TetrominoTransmission.L_TETROMINO_270, TetrominoTransmission.O_TETROMINO, TetrominoTransmission.J_TETROMINO_90],
            [TetrominoTransmission.Z_TETROMINO_90, TetrominoTransmission.T_TETROMINO_270],
            [TetrominoTransmission.J_TETROMINO_270],
            [TetrominoTransmission.L_TETROMINO_90],
            [TetrominoTransmission.S_TETROMINO_90, TetrominoTransmission.T_TETROMINO_90]]

  @staticmethod
  def get_surface_array_l2():
    return [[ [TetrominoTransmission.L_TETROMINO_180, TetrominoTransmission.J_TETROMINO_180, TetrominoTransmission.T_TETROMINO_180],
              [TetrominoTransmission.S_TETROMINO],
              [TetrominoTransmission.J_TETROMINO]],
            [ [TetrominoTransmission.L_TETROMINO], [], []],
            [ [], [], []],
            [ [], [], []],
            [ [TetrominoTransmission.Z_TETROMINO],
              [TetrominoTransmission.T_TETROMINO], []]]
