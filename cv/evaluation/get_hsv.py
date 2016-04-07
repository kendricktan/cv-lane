# Import parent path (to get settings.py)
import os.path, sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))

import cv2
import numpy as np
from picamera.array import PiRGBArray
from picamera import PiCamera
from settings import *

WIDTH = CAMERA_WIDTH
HEIGHT = CAMERA_HEIGHT

x_co = 0
y_co = 0

def on_mouse(event,x,y,flag,param):
    global x_co, y_co
    x_co = x
    y_co = y

# Get video feed
camera = PiCamera()
camera.resolution = (WIDTH, HEIGHT)
camera.awb_mode = AWB_MODE
camera.awb_gains = AWB_GAINS
camera.exposure = EXPOSURE
camera.shutter_spped = SHUTTER
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(CAMERA_WIDTH, CAMERA_HEIGHT))
stream = camera.capture_continuous(rawCapture, format='bgr', use_video_port=True)

cv2.namedWindow('camera')

for (i, f) in enumerate(stream):
    frame = f.array
    #frame = cv2.imread('../../img/highway.jpg')

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    cv2.setMouseCallback("camera", on_mouse, 0)

    try:
        values = hsv[y_co, x_co]
        print('H:', values[0], '\tS:', values[1], '\tV:', values[2])
    except:
        pass

    rawCapture.truncate(0)

    cv2.imshow('camera', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

stream.close()
rawCapture.close()
camera.close()
cv2.destroyAllWindows()
