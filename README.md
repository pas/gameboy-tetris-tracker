# gameboy-tetris-tracker

The current version of this tracker takes screenshots of a specific location of your screen where your tetris game is displayed. Afterwards tries to retrieve information from this image. Unfortunately at the moment it is not possible to read the live feed directly. OpenCV is not able to read an OBS virtual cam feed directly.

This project is in a early prototyping phase. You will need to tweek it to make it work. It is currently developed on Windows 11. There is no guarantee that it will run on other operating systems.

This project came to light during a conversation with Tolstoj. Many ideas where either directly provided by Tolstoj or are derivates of those ideas. All tile images where provided by him! Thanks a lot!

## Preconditions

You'll need to have tesseract installed. 

### Windows
For windows user the UB Mannheim provides a windows version: https://hypi.app/assets/wp/wp-content/uploads/2019/10/wiki/

## Start the program 

    python main.py

## Grab bounding box

Select in Menu Others -> Retrieve bounding box

You'll see an image of your screen. Drag from left top corner to bottom right corner. Make sure there is a distinguishable black border around the image. For good results have the select type screen open in your tetris game.

After selection you'll see a green border around the selected part. Restart if not good. Close window if selection is correct.
  
The selected bounding box is automatically stored in config.yml. You don't need to repeat this step is you don't move window from which you grab the screenshot.

The program is currently really sensitive to imprecise bounding boxes. If it does not categorize the minos correctly then it is probably because of the bounding box.

# Start tracker
Press start on the main screen. Press stop to stop tracking.

# Wanna share your scores and play Gameboy Tetris with amazing people?
Join our discord server! https://discord.gg/TjrSDzmb