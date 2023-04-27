# gameboy-tetris-tracker

This project came to light during a conversation with Tolstoj. Many ideas where either directly provided by Tolstoj or are derivates of those ideas. All tile images where provided by him! Thanks a lot!

This project is in a very early prototyping phase. You will need to tweek it to make it work, for example the bounding boxes for the screenshots are hardcoded. You will have to adapt them by hand.

## grabbing the bounding boxes

Use a still image with your setting where the video will be shown on the screen. Run the program:

    python retrieve_bounding_box.py

Drag from left top corner to bottom right corner. Copy bounding boxes out of your console into config.yml file.

## Check if bounding boxes are correct

    python check.py

Then look at the screenshots at screenshots/ folder. 

Do the fully show the scores and the lines without any borders? If not, reset your bounding boxes. 

Do they show the full playfield with brick borders? If not, reset your bounding boxes. Best do it by correcting the values by hand.

Do they show the preview box without any borders? Be aware that the preview box needs to be tiled in four time four pieces. Setting this bounding box correct is normally quite tricky.
  
The program is currently really sensitive to imprecise bounding boxes especially the playfield and the preview part. If it does not categorize the minos correctly then it is probably because of the bounding boxes.

# Wanna play Gameboy Tetris?
Join our discord server! https://discord.gg/TjrSDzmb