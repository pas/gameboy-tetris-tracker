# Trained with the following commands:

tesseract --psm 8 tetris.font.exp0.tif tetris.font.exp0 nobatch box.train
unicharset_extractor tetris.font.exp0.box
shapeclustering -F font_properties -U unicharset -O tetris.unicharset tetris.font.exp0.tr
mftraining -F font_properties -U unicharset -O tetris.unicharset tetris.font.exp0.tr
cntraining tetris.font.exp0.tr

# Boxes

Boxes where created with JTessBoxCreator:
1) Tools -> Merge TIFF


# Version history
## Version 4
Added larger 84x84 image of 1 as it was not able to recognize it.