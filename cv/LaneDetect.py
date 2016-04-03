import cv2
import numpy as np

class DRCLaneDetect(object):
    def __init__(self, resolution):
        self.height = resolution[0]
        self.width = resolution[1]

        # Padding for our width and stuff
        self.height_dif = int(self.height/3)
        self.width_dif = int(self.width/4)

    def set_frame(self, frame):
        return

    def update(self):
        return

