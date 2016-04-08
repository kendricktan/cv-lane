# Import parent path (to get settings.py)
import os.path, sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))

import cv2
import numpy as np
import time
from picamera.array import PiRGBArray
from picamera import PiCamera
from settings import *

WIDTH = CAMERA_WIDTH
HEIGHT = CAMERA_HEIGHT

x_co = 0
y_co = 0

hsv = None
frame= None

# Mouse event handler
def on_mouse(event,x,y,flag,param):
    # Where we'll be writing and getting our values from
    global hsv, frame
    if event == cv2.EVENT_LBUTTONDBLCLK:
        # Circle to indicate hsv location, and update frame
        cv2.circle(frame, (x, y), 3, (0, 0, 255))
        cv2.imshow('camera', frame)

        # Print values
        values = hsv[y, x]
        print('H:', values[0], '\tS:', values[1], '\tV:', values[2])

# Get video feed and set camera parameters
camera = PiCamera()
camera.resolution = (WIDTH, HEIGHT)
camera.awb_mode = AWB_MODE
camera.awb_gains = AWB_GAINS
camera.exposure = EXPOSURE
camera.shutter_spped = SHUTTER
camera.framerate = 32

rawCapture = PiRGBArray(camera, size=(CAMERA_WIDTH, CAMERA_HEIGHT))

stream = camera.capture_continuous(rawCapture, format='bgr', use_video_port=True)

# Warm camera up
time.sleep(2.0)

# Cv window
cv2.namedWindow('camera')

for (i, f) in enumerate(stream):
    frame = f.array

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Set mouse event handler
    cv2.setMouseCallback("camera", on_mouse, 0)
    cv2.imshow('camera', frame)

    rawCapture.truncate(0)

    # Set keyboard event handler
    key = cv2.waitKey(0) & 0xFF
    if key == ord('q'):
        break

stream.close()
rawCapture.close()
camera.close()
cv2.destroyAllWindows()
