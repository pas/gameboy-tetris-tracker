# gameboy-tetris-tracker

This project is in a prototyping phase. You will need to tweek it to make it work. It is currently developed on Windows 11. There is no guarantee that it will run on other operating systems (and if I'm honest not even on Windows 11...).

This project came to light during a conversation with Tolstoj. Many ideas where either directly provided by Tolstoj or are derivates of those ideas. All tile images where provided by him! Thanks a lot!

Currently, everything done in is project is free to use but no guarantees given for anything.

## Preconditions
You'll need to have tesseract installed. 

### Windows
This program was tested with version 5.3.1 of tesseract. You can download an installer by UB Mannheim for windows here: https://digi.bib.uni-mannheim.de/tesseract/?C=M;O=A. Please make sure that the tesseract exe is in your path variable. 

## Python
Run on version 3.11 of python.

## Packages
mss 9.0.1
matplotlib 3.8.0
Pillow 10.2.0
opencv-python 4.9.0.80
numpy 1.26.4
PyYAML 6.0.1
PySimpleGUI 4.60.5
pytesseract 0.3.10
typing_extensions 4.9.0

## Start the program 

    python main.py

A window should appear.

## Usage
There are currently three ways to use this tool. Selected usage from menu under "Capture".

Either this tracker takes screenshots of a specific location of your screen where your tetris game is displayed or it uses direct input from the interceptor or it used the obs virtual cam.

### Screenshot
Select in Menu -> Capture -> screen

Select in Menu -> Others -> Retrieve bounding box

You'll see an image of your screen. Drag from left top corner to bottom right corner. Make sure there is a distinguishable black border around the image. For good results have the select type screen open in your tetris game.

After selection you'll see a green border around the selected part. Restart if not good. Close window if selection is correct.
  
The selected bounding box is automatically stored in config.yml. You don't need to repeat this step is you don't move window from which you grab the screenshot.

The program is sensitive to imprecise bounding boxes. If it does not categorize the minos correctly then it is probably because of the bounding box.

### OBS
Select in Menu -> Capture -> obs

Select in Menu -> Others -> Camera selection

You'll see a popup. Select image that shows the obs virtual cam.

Select in Menu Others -> Retrieve bounding box
=> See "screenshot" for more information

### Interceptor
This is a newer implementation and will probably not work properly.

Select in Menu -> Capture -> Interceptor

Select in Menu -> Others -> Camera. Select the interceptor image.

## Start tracker
Press start on the main screen. Press stop to stop tracking. 

You'll need to monitor your command line to see if everything works as intended.

## Configuration config.yml
capturer: obs|screen|interceptor
rom_version: original|gamescom # The gamescom version has the score shifted one tile to the right
plotter: piece_distribution|progress 

## Database
Currently, all data is stored in an Sqlite database stored at screenshots/tetris.db.

## Known Bugs
When starting the program, the current capture mode is not shown when clicking on the menu. It only shows "(x)" once you've select one.

Starting only on menu screen possible. Starting on end screen and during game throws error.

When OBS is open then there are sometimes problems with acquiring access to the camera as OBS is attempting the same. Same when other programs are trying to use the camera.

# Wanna share your scores and play Gameboy Tetris with amazing people?
Join our discord server! https://discord.gg/TjrSDzmb