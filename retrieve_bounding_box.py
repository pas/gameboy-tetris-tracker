import cv2
from mss import mss
from PIL import Image, ImageOps
import numpy as np

class BoundingBoxWidget(object):
    """
    By nathancy
    From https://stackoverflow.com/a/55153612
    Adapted by Pas
    CC BY-SA 4.0 (by StackOverflow)
    """

    def __init__(self):
        sct = mss()
        monitor_screenshot = sct.grab(monitor=sct.monitors[0])
        monitor_screenshot = np.array(monitor_screenshot)

        self.original_image = monitor_screenshot
        self.clone = self.original_image.copy()

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
            print('top left: {}, bottom right: {}'.format(self.image_coordinates[0], self.image_coordinates[1]))
            print("top: {}\nleft: {}\nwidth: {}\nheight: {}".format(self.image_coordinates[0][1], self.image_coordinates[0][0], self.image_coordinates[1][0] - self.image_coordinates[0][0], self.image_coordinates[1][1] - self.image_coordinates[0][1]))

            # Draw rectangle
            cv2.rectangle(self.clone, self.image_coordinates[0], self.image_coordinates[1], (36,255,12), 2)
            cv2.imshow("image", self.clone)

        # Clear drawing boxes on right mouse button click
        elif event == cv2.EVENT_RBUTTONDOWN:
            self.clone = self.original_image.copy()

    def show_image(self):
        return self.clone

if __name__ == '__main__':
    boundingbox_widget = BoundingBoxWidget()
    cv2.imshow('image', boundingbox_widget.show_image())
    while cv2.getWindowProperty('image', 0) >= 0:
        cv2.imshow('image', boundingbox_widget.show_image())
        key = cv2.waitKey(1)

        # Close program with keyboard 'q'
        if key == ord('q'):
            cv2.destroyAllWindows()
            exit(1)