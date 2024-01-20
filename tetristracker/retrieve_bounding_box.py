import cv2
import yaml
from mss import mss
from PIL import Image
import numpy as np
from tetristracker.image.image_manipulator import trim
from tetristracker.helpers.config import Config

class BoundingBoxWidget(object):
    """
    By nathancy
    From https://stackoverflow.com/a/55153612
    Adapted by Pas
    CC BY-SA 4.0 (by StackOverflow)
    """

    def __init__(self):
        sct = mss()
        print(sct.monitors[0])
        monitor_screenshot = sct.grab(sct.monitors[0])
        monitor_screenshot = np.array(Image.fromarray(np.array(monitor_screenshot)).convert("RGB"))

        self.original_image = monitor_screenshot
        self.clone = self.original_image.copy()

        print("Select by click and drag from the top left to the bottom right. Make sure there"
              + " is a distinguishable black border around the image. This gives the best results.")

        cv2.namedWindow('image')
        cv2.setMouseCallback('image', self.extract_coordinates)

        # Bounding box reference points
        self.image_coordinates = []

    def extract_coordinates(self, event, x, y, flags, parameters):
        # Record starting (x,y) coordinates on left mouse button click
        if event == cv2.EVENT_LBUTTONDOWN:
            self.image_coordinates = [(x,y)]

        # Record ending (x,y) coordintes on left mouse button release
        elif event == cv2.EVENT_LBUTTONUP:
            self.image_coordinates.append((x,y))

            print(self.image_coordinates)
            cropped = self.crop()
            _, top, bottom, left, right = trim(cropped)
            self.image_coordinates[0] = (self.image_coordinates[0][0]+left, self.image_coordinates[0][1]+top)
            self.image_coordinates[1] = (self.image_coordinates[1][0]-right, self.image_coordinates[1][1]-bottom)
            print('top left: {}, bottom right: {}'.format(self.image_coordinates[0], self.image_coordinates[1]))

            top = self.image_coordinates[0][1]
            left = self.image_coordinates[0][0]
            width = self.image_coordinates[1][0] - self.image_coordinates[0][0]
            height = self.image_coordinates[1][1] - self.image_coordinates[0][1]

            print("top: {}\nleft: {}\nwidth: {}\nheight: {}".format(top,
                                                                    left,
                                                                    width,
                                                                    height))

            bounding_box = {'top': self.image_coordinates[0][1],
                            'left': self.image_coordinates[0][0],
                            'width': self.image_coordinates[1][0] - self.image_coordinates[0][0],
                            'height': self.image_coordinates[1][1] - self.image_coordinates[0][1]}

            config = Config()
            config.set_bounding_box(bounding_box)

            # Draw rectangle
            cv2.rectangle(self.clone, self.image_coordinates[0], self.image_coordinates[1], (36,255,12), 2)
            cv2.imshow("image", self.clone)

        # Clear drawing boxes on right mouse button click
        elif event == cv2.EVENT_RBUTTONDOWN:
            self.clone = self.original_image.copy()

    def show_image(self):
        return self.clone

    def crop(self):
        return self.clone[self.image_coordinates[0][1]:self.image_coordinates[1][1],
                  self.image_coordinates[0][0]:self.image_coordinates[1][0]].copy()

def run():
    boundingbox_widget = BoundingBoxWidget()
    cv2.imshow('image', boundingbox_widget.show_image())
    # This needs some work...
    try:
        while cv2.getWindowProperty('image', 0) >= 0:
            cv2.imshow('image', boundingbox_widget.show_image())
            key = cv2.waitKey(1)

            # Close program with keyboard 'q'
            if key == ord('q'):
                cv2.destroyWindow('image')
    except:
        pass # Don't do anything here...



if __name__ == '__main__':
    run()