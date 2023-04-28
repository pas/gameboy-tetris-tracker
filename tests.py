import unittest
from playfield_processor import PlayfieldProcessor, PreviewProcessor, PlayfieldRecreator, GameboyViewProcessor, NumberProcessor
from PIL import Image
import numpy as np
from tile_recognizer import TileRecognizer, Tile, Tiler
from csvfile import CSVReader

class TestPlayfieldProcessor(unittest.TestCase):

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
      print(score_image.shape)
      score_image = self.untile(score_image)
      print(score_image.shape)
      number_processor = NumberProcessor(score_image)
      score = number_processor.get_number()
      self.assertEqual(39, score)

  def untile(self, image):
      shape = image.shape
      nr_of_tiles_height = shape[0]
      nr_of_tiles_width = shape[1]
      tile_width = shape[2]
      tile_height = shape[3]
      color_channels = shape[4]
      return image.swapaxes(1, 2).reshape(nr_of_tiles_height*tile_height, nr_of_tiles_width*tile_width, color_channels)

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
    tiler = Tiler(18, 12, image)
    assert(tiler.adapted_image.shape[0] == 18)
    assert(tiler.adapted_image.shape[1] == 12)
    self.assertEqual(tiler.tile_height, 53)
    self.assertEqual(tiler.tile_width, 53)

  def test_preview_processor_z(self):
    image = np.array(Image.open("test/preview/z-tetromino-preview.png").convert('RGB'))
    preview_processor = PreviewProcessor(image)
    result = preview_processor.run()
    self.assertEqual(result, TileRecognizer.Z_MINO)

  def test_preview_processor_l(self):
    image = np.array(Image.open("test/preview/l-tetromino-preview.png").convert('RGB'))
    preview_processor = PreviewProcessor(image)
    result = preview_processor.run()
    self.assertEqual(result, TileRecognizer.L_MINO)

  def test_preview_processor_j(self):
    image = np.array(Image.open("test/preview/j-tetromino-preview.png").convert('RGB'))
    preview_processor = PreviewProcessor(image)
    result = preview_processor.run()
    self.assertEqual(result, TileRecognizer.J_MINO)

  def test_preview_processor_s(self):
    image = np.array(Image.open("test/preview/s-tetromino-preview.png").convert('RGB'))
    preview_processor = PreviewProcessor(image)
    result = preview_processor.run()
    self.assertEqual(result, TileRecognizer.S_MINO)

  def test_preview_processor_o(self):
    image = np.array(Image.open("test/preview/o-tetromino-preview.png").convert('RGB'))
    preview_processor = PreviewProcessor(image)
    result = preview_processor.run()
    self.assertEqual(result, TileRecognizer.O_MINO)

  def test_preview_processor_i(self):
    image = np.array(Image.open("test/preview/i-tetromino-preview.png").convert('RGB'))
    preview_processor = PreviewProcessor(image)
    result = preview_processor.run()
    self.assertEqual(result, TileRecognizer.I_MINO_SIMPLE)

  def test_preview_processor_t(self):
    image = np.array(Image.open("test/preview/t-tetromino-preview.png").convert('RGB'))
    preview_processor = PreviewProcessor(image)
    result = preview_processor.run()
    self.assertEqual(result, TileRecognizer.T_MINO)

  def test_playfield_recreator(self):
    recreator = PlayfieldRecreator()
    playfield = self.create_testing_array_s2()
    recreator.recreate(playfield, 'test/screenshot-playfield-recreation.png')

  def test_csvreader(self):
    reader = CSVReader("20230427103034")
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

  def create_array_only_hits(self, array):
    array = array.copy()
    array[array > -99] = 1
    array[array == -99] = 0
    return array

if __name__ == '__main__':
  unittest.main()