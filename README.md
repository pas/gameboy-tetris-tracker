# gameboy-tetris-tracker

This project is in an early prototyping phase. You will need to tweek it to make it work. It is currently developed on Windows 11. There is no guarantee that it will run on other operating systems (and if I'm honest not even on Windows 11...).

This project came to light during a conversation with Tolstoj. Many ideas where either directly provided by Tolstoj or are derivates of those ideas. All tile images where provided by him! Thanks a lot!

Currentlyy everything done in is project is free to use but no guarantees given for anything.

## Preconditions
You'll need to have tesseract installed. 

### Windows
This program was tested with version 5.3.1 of tesseract. You can download an installer by UB Mannheim for windows here: https://digi.bib.uni-mannheim.de/tesseract/?C=M;O=A. Please make sure that the tesseract exe is in your path variable. 

## Python
Run on version 3.10 of python.

## Packages
mss 9.0.1
matplotlib 3.8.0
Pillow 10.0.1
opencv-python 4.8.1.78
numpy 1.26.0
PyYAML 6.0.1
PySimpleGUI 4.60.5
pythesseract 0.3.10

## Start the program 

    python main.py

## Usage
There are currently two ways to use this tool. Either it this tracker takes screenshots of a specific location of your screen where your tetris game is displayed or it uses direct input from the interceptor. Unfortunately at the moment it is not possible to read the feed from OBS virtual cam. 

### Screenshot technic
Select in Menu Capture -> Screenshot

Select in Menu Others -> Retrieve bounding box

You'll see an image of your screen. Drag from left top corner to bottom right corner. Make sure there is a distinguishable black border around the image. For good results have the select type screen open in your tetris game.

After selection you'll see a green border around the selected part. Restart if not good. Close window if selection is correct.
  
The selected bounding box is automatically stored in config.yml. You don't need to repeat this step is you don't move window from which you grab the screenshot.

The program is sensitive to imprecise bounding boxes. If it does not categorize the minos correctly then it is probably because of the bounding box.

### Interceptor technic
This is a newer implementation and will probably not work properly.

Select in Menu -> Capture -> Interceptor

Select in Menu -> Others -> Camera. Select the interceptor image.

## Start tracker
Press start on the main screen. Press stop to stop tracking.

# Wanna share your scores and play Gameboy Tetris with amazing people?
Join our discord server! https://discord.gg/TjrSDzmb