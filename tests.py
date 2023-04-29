import unittest
from playfield_processor import PlayfieldProcessor, Playfield
from preview_processor import PreviewProcessor
from gameboy_view_processor import GameboyViewProcessor
from number_processor import NumberProcessor
from playfield_recreator import PlayfieldRecreator
from gameboy_image import GameboyImage
from PIL import Image
import numpy as np
from tile_recognizer import TileRecognizer, Tile, Tiler
from runner import Runner
from csvfile import CSVReader

class MockCSVWriter():
    def __init__(self):
        self.calls = 0

    def write(self, accepted_score, accepted_lines, current_preview, current_playfield):
        self.calls += 1

# need to overwrite the grab_image
# method to inject an image
class TestRunner(Runner):
    def __init__(self):
        super().__init__()
        self.csv_file = MockCSVWriter()

    def grab_image(self, bounding_box):
        return np.array(Image.open("test/gameboy-pause-full-view.png").convert('RGB'))

    def calls(self):
        return self.csv_file.calls

class TestPlayfieldProcessor(unittest.TestCase):
  def test_playfield(self):
    playfield = Playfield(self.create_testing_array_full_line())
    self.assertSequenceEqual(playfield.playfield_array[11].tolist(), [   3 ,   3 ,   3 ,   9 ,  10,  10,  11,   3,   3,   3 ])
    playfield.full_row_replacement()
    self.assertSequenceEqual(playfield.playfield_array[11].tolist(), [ -99 , -99 , -99 , -99 , -99, -99, -99, -99, -99, -99 ])

  def test_runner_on_pause(self):
      runner = TestRunner()
      runner.run(times=1)
      # During pause the csv writer should not be called
      self.assertEqual(runner.calls(),0)

  def test_gameboy_view_processor_on_pause(self):
      image = np.array(Image.open("test/gameboy-pause-full-view.png").convert('RGB'))
      processor = GameboyViewProcessor(image)
      continue_image = processor.get_continue()
      gameboy_image = GameboyImage(continue_image, 8, 4, 53, 53, is_tiled=True)
      gameboy_image.untile()
      number_process = NumberProcessor(gameboy_image.image)
      self.assertEqual(71006 ,number_process.get_number())

  def test_gameboy_image(self):
    processor = self.create_gameboy_view_processor()

    #get a tiled 4x4 image
    preview_image = processor.get_preview()

    gameboy_image = GameboyImage(preview_image, 4, 4, 53, 53, is_tiled=True)
    image = gameboy_image.untile()
    self.assertEqual(4*53, image.shape[0])
    self.assertEqual(4*53, image.shape[1])
    self.assertEqual(3, image.shape[2])

    image = gameboy_image.tile()
    self.assertEqual(4, image.shape[0])
    self.assertEqual(4, image.shape[1])
    self.assertEqual(53, image.shape[2])
    self.assertEqual(53, image.shape[3])
    self.assertEqual(3, image.shape[4])

  def create_gameboy_view_processor(self):
    image = np.array(Image.open("test/gameboy-full-view.png").convert('RGB'))
    return GameboyViewProcessor(image)

  def test_combine_gameboy_view_processor_and_other_processors(self):
    processor = self.create_gameboy_view_processor()

    preview_image = processor.get_preview()
    preview_processor = PreviewProcessor(preview_image, image_is_tiled=True)
    preview = preview_processor.run()
    self.assertEqual(preview, TileRecognizer.T_MINO)

    score_image = processor.get_score()
    score_image = GameboyImage(score_image, score_image.shape[0], score_image.shape[1],
                               score_image.shape[2], score_image.shape[3], is_tiled=True)
    score_image.save("test/")
    score_image.untile()
    number_processor = NumberProcessor(score_image.image)
    score = number_processor.get_number()
    self.assertEqual(39, score)

    lines_image = processor.get_lines()
    lines_image = GameboyImage(lines_image, lines_image.shape[0], lines_image.shape[1],
                               lines_image.shape[2], lines_image.shape[3], is_tiled=True)
    lines_image.untile()
    number_processor = NumberProcessor(lines_image.image)
    lines = number_processor.get_number()
    self.assertEqual(0, lines)

    level_image = processor.get_level()
    level_image = GameboyImage(level_image, level_image.shape[0], level_image.shape[1],
                               level_image.shape[2], level_image.shape[3], is_tiled=True)
    level_image.untile()
    number_processor = NumberProcessor(level_image.image)
    level = number_processor.get_number()
    self.assertEqual(0, level)

    playfield_image = processor.get_playfield()

  def test_gameboy_view_processor(self):
      processor = self.create_gameboy_view_processor()

      playfield = processor.get_playfield()
      self.assertEqual(playfield.shape[0], 18)
      self.assertEqual(playfield.shape[1], 10)

      preview = processor.get_preview()
      self.assertEqual(preview.shape[0], 4)
      self.assertEqual(preview.shape[1], 4)

      score = processor.get_score()
      self.assertEqual(score.shape[0], 1)
      self.assertEqual(score.shape[1], 6)

      lines = processor.get_lines()
      self.assertEqual(lines.shape[0], 1)
      self.assertEqual(lines.shape[1], 3)


  def test_l_mino(self):
    recognizer = TileRecognizer()
    tile = np.array(Image.open("test/debug/L-mino-1.png").convert('RGB'))
    result = recognizer.recognize(tile)

    self.assertEqual(result, 3)

  def test_t_mino(self):
    recognizer = TileRecognizer()
    tile = np.array(Image.open("test/debug/T-mino-1.png").convert('RGB'))

    result = recognizer.recognize(tile)

    self.assertEqual(result, 4)

  def test_tile(self):
    tile_image = np.array(Image.open("test/debug/T-mino-1.png").convert('RGB'))
    tile = Tile(tile_image);
    tile.store("test/debug/T-mino-1-adapted.png")

  def test_tiler(self):
    image = np.array(Image.open("test/scenario-2-high-res.png").convert('RGB'))
    tiler = Tiler(18, 10, image)
    assert(tiler.adapted_image.shape[0] == 18)
    assert(tiler.adapted_image.shape[1] == 10)
    self.assertEqual(tiler.tile_height, 53)
    self.assertEqual(tiler.tile_width, 53)

  def test_preview_processor_ambigous(self):
    image = np.array(Image.open("test/preview/t-to-l-tetromino-transition-preview.png").convert('RGB'))
    preview_processor = PreviewProcessor(image)
    preview_processor.run()
    self.assertTrue(preview_processor.ambigous)

  def test_preview_processor_z(self):
    image = np.array(Image.open("test/preview/z-tetromino-preview.png").convert('RGB'))
    preview_processor = PreviewProcessor(image)
    result = preview_processor.run()
    self.assertEqual(result, TileRecognizer.Z_MINO)
    self.assertFalse(preview_processor.ambigous)

  def test_preview_processor_l(self):
    image = np.array(Image.open("test/preview/l-tetromino-preview.png").convert('RGB'))
    preview_processor = PreviewProcessor(image)
    result = preview_processor.run()
    self.assertEqual(result, TileRecognizer.L_MINO)
    self.assertFalse(preview_processor.ambigous)

  def test_preview_processor_j(self):
    image = np.array(Image.open("test/preview/j-tetromino-preview.png").convert('RGB'))
    preview_processor = PreviewProcessor(image)
    result = preview_processor.run()
    self.assertEqual(result, TileRecognizer.J_MINO)
    self.assertFalse(preview_processor.ambigous)

  def test_preview_processor_s(self):
    image = np.array(Image.open("test/preview/s-tetromino-preview.png").convert('RGB'))
    preview_processor = PreviewProcessor(image)
    result = preview_processor.run()
    self.assertEqual(result, TileRecognizer.S_MINO)
    self.assertFalse(preview_processor.ambigous)

  def test_preview_processor_o(self):
    image = np.array(Image.open("test/preview/o-tetromino-preview.png").convert('RGB'))
    preview_processor = PreviewProcessor(image)
    result = preview_processor.run()
    self.assertEqual(result, TileRecognizer.O_MINO)
    self.assertFalse(preview_processor.ambigous)

  def test_preview_processor_i(self):
    image = np.array(Image.open("test/preview/i-tetromino-preview.png").convert('RGB'))
    preview_processor = PreviewProcessor(image)
    result = preview_processor.run()
    self.assertEqual(result, TileRecognizer.I_MINO_SIMPLE)
    self.assertFalse(preview_processor.ambigous)

  def test_preview_processor_t(self):
    image = np.array(Image.open("test/preview/t-tetromino-preview.png").convert('RGB'))
    preview_processor = PreviewProcessor(image)
    result = preview_processor.run()
    self.assertEqual(result, TileRecognizer.T_MINO)
    self.assertFalse(preview_processor.ambigous)

  def test_playfield_recreator(self):
    recreator = PlayfieldRecreator()
    playfield = self.create_testing_array_s2()
    recreator.recreate(playfield, 'test/screenshot-playfield-recreation.png')

  def test_csvreader(self):
    reader = CSVReader("20230427212001")
    reader.to_image("test/recreation/")

  def full_image(self, image_path, test):
    image = np.array(Image.open(image_path).convert('RGBA'))
    playfield = PlayfieldProcessor(image)
    result = playfield.run()

    result = np.array(result).reshape(18, 10)
    difference = result - test
    hits = result.copy()
    # set edge cases to no tile
    hits[hits > 11] = -99
    hits[hits > -99] = 1
    hits[hits == -99] = 0
    hits = hits - self.create_array_only_hits(test)
    false_negatives = hits.copy()
    false_negatives[hits == 1] = 0
    false_negatives[hits == -1] = 1
    performance = np.sum(false_negatives)
    self.assertEqual(0, performance, "Some false negatives")

    false_positives = hits.copy()
    false_positives[hits == -1] = 0
    performance = np.sum(false_positives)

    if (performance > 0):
      print(result)
      print(difference)

    self.assertEqual(0, performance, "Some false positives")

    arr = difference.copy()
    arr[arr > 0] = 1
    arr[arr < 0] = 1

    performance = np.sum(arr)
    if (performance > 0):
      print(arr)
    self.assertEqual(0, performance, "Some miscategorized minos")

  def test_second_scenario(self):
    self.full_image("test/scenario-2-high-res.png", self.create_testing_array_s2())

  def test_first_scenario(self):
    self.full_image("test/scenario-1-high-res.png", self.create_testing_array_s1())

  def create_testing_array_s2(self):
    array = [ [ -99 , -99 , -99 , -99 , -99, -99, -99, -99, -99, -99 ],
              [ -99 , -99 , -99 ,   3 ,   3,   3, -99, -99, -99, -99 ],
              [ -99 , -99 , -99 ,   3 , -99, -99, -99, -99, -99, -99 ],
              [ -99 , -99 , -99 , -99 ,   2,   2, -99, -99, -99,   4 ],
              [ -99 , -99 , -99 , -99 ,   2,   2, -99,   5,   4,   4 ],
              [ -99 ,   2 ,   2 , -99 ,   5,   5, -99,   5,   5,   4 ],
              [ -99 ,   2 ,   2 ,   5 ,   5, -99,   5,   5,   5, -99 ],
              [ -99 , -99 ,   1 ,   1 , -99,   5,   5, -99, -99, -99 ],
              [ -99 , -99 , -99 ,   1 ,   1,   1, -99, -99, -99, -99 ],
              [ -99 , -99 , -99 , -99 ,   1,   1, -99, -99, -99, -99 ],
              [ -99 , -99 , -99 , -99 ,   1, -99, -99, -99, -99, -99 ],
              [ -99 , -99 , -99 , -99 ,   2,   2, -99, -99, -99, -99 ],
              [ -99 , -99 , -99 , -99 ,   2,   2, -99, -99, -99, -99 ],
              [ -99 , -99 , -99 , -99 ,   3,   3, -99, -99, -99, -99 ],
              [ -99 , -99 , -99 , -99 , -99,   3, -99, -99, -99, -99 ],
              [ -99 , -99 , -99 , -99 , -99,   3, -99, -99,   2,   2 ],
              [ -99 , -99 , -99 , -99 ,   1,   1, -99, -99,   2,   2 ],
              [ -99 , -99 ,   5 , -99 ,   6,   1,   1, -99,   2,   2 ] ]
    return (np.array(array))

  def create_testing_array_s1(self):
    array = [ [ -99 , -99 , -99 , -99 , -99, -99, -99, -99, -99, -99 ],
              [ -99 , -99 , -99 , -99 , -99, -99, -99, -99, -99, -99 ],
              [ -99 , -99 , -99 , -99 , -99, -99, -99, -99, -99, -99 ],
              [ -99 , -99 , -99 , -99 , -99, -99, -99, -99, -99, -99 ],
              [ -99 , -99 , -99 , -99 , -99, -99, -99, -99, -99, -99 ],
              [ -99 , -99 , -99 , -99 , -99, -99, -99, -99, -99, -99 ],
              [ -99 , -99 , -99 , -99 , -99, -99, -99, -99, -99, -99 ],
              [ -99 , -99 , -99 ,   1 ,   1, -99, -99, -99, -99, -99 ],
              [ -99 , -99 , -99 , -99 ,   1,   1, -99, -99, -99, -99 ],
              [   0 ,   0 ,   0 , -99 , -99, -99, -99, -99, -99, -99 ],
              [ -99 , -99 ,   0 , -99 , -99, -99, -99, -99, -99, -99 ],
              [   3 ,   3 ,   3 ,   9 ,  10,  10,  11, -99, -99, -99 ],
              [   3 , -99 , -99 ,   4 ,   4,   4, -99, -99, -99, -99 ],
              [   4 , -99 , -99 , -99 ,   4, -99, -99,   1,   1, -99 ],
              [   4 ,   4 , -99 ,   3 ,   3,   3, -99, -99,   1,   1 ],
              [   4 , -99 , -99 ,   3 , -99, -99, -99, -99, -99,   4 ],
              [   2 ,   2 , -99 ,   1 ,   1, -99, -99, -99,   4,   4 ],
              [   2 ,   2 , -99 , -99 ,   1,   1, -99, -99, -99,   4 ] ]
    return (np.array(array))

  def create_testing_array_full_line(self):
    array = [ [ -99 , -99 , -99 , -99 , -99, -99, -99, -99, -99, -99 ],
              [ -99 , -99 , -99 , -99 , -99, -99, -99, -99, -99, -99 ],
              [ -99 , -99 , -99 , -99 , -99, -99, -99, -99, -99, -99 ],
              [ -99 , -99 , -99 , -99 , -99, -99, -99, -99, -99, -99 ],
              [ -99 , -99 , -99 , -99 , -99, -99, -99, -99, -99, -99 ],
              [ -99 , -99 , -99 , -99 , -99, -99, -99, -99, -99, -99 ],
              [ -99 , -99 , -99 , -99 , -99, -99, -99, -99, -99, -99 ],
              [ -99 , -99 , -99 , -99 , -99, -99, -99, -99, -99, -99 ],
              [ -99 , -99 , -99 , -99 , -99,  -99, -99, -99, -99, -99 ],
              [   0 ,   0 ,   0 , -99 , -99, -99, -99, -99, -99, -99 ],
              [ -99 , -99 ,   0 , -99 , -99, -99, -99, -99, -99, -99 ],
              [   3 ,   3 ,   3 ,   9 ,  10,  10,  11,   3,   3,   3 ],
              [   3 , -99 , -99 ,   4 ,   4,   4, -99,   3, -99, -99 ],
              [   4 , -99 , -99 , -99 ,   4, -99, -99,   1,   1, -99 ],
              [   4 ,   4 , -99 ,   3 ,   3,   3, -99, -99,   1,   1 ],
              [   4 , -99 , -99 ,   3 , -99, -99, -99, -99, -99,   4 ],
              [   2 ,   2 , -99 ,   1 ,   1, -99, -99, -99,   4,   4 ],
              [   2 ,   2 , -99 , -99 ,   1,   1, -99, -99, -99,   4 ] ]
    return (np.array(array))

  def create_array_only_hits(self, array):
    array = array.copy()
    array[array > -99] = 1
    array[array == -99] = 0
    return array

if __name__ == '__main__':
  unittest.main()