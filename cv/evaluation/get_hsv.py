# Import parent path (to get settings.py)
import os.path, sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
import argparse
import cv2
import numpy as np
import time
from picamera.array import PiRGBArray
from picamera import PiCamera
from settings import *

parser = argparse.ArgumentParser(description='get_hsv values')
parser.add_argument('--auto', help='use auto settings instead of the ones from settings.py')
args = parser.parse_args()

WIDTH = CAMERA_WIDTH
HEIGHT = CAMERA_HEIGHT

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

# If we're using custom settings
if not args.auto:
    camera.awb_gains = AWB_GAINS
    camera.awb_mode = AWB_MODE
    camera.exposure_mode = EXPOSURE_MODE
    camera.exposure_compensation = EXPOSURE_COMPENSATION
    camera.shutter_spped = SHUTTER
    camera.saturation = SATURATIONo_stabilization = VIDEO_STABALIZATION
    camera.video_stabilization = VIDEO_STABALIZATION
    camera.framerate = 32

rawCapture = PiRGBArray(camera, size=(CAMERA_WIDTH, CAMERA_HEIGHT))

stream = camera.capture_continuous(rawCapture, format='bgr', use_video_port=True)

# Warm camera up
time.sleep(2.0)

# Print camera settings (if in auto)
if args.auto:
    print('awb_gain:', camera.awb_gains)
    print('awb_mode:', camera.awb_mode)
    print('exposure_compensation:', camera.exposure_mode)
    print('exposure_compensation:', camera.exposure_compensation)
    print('shutter_speed:', camera.shutter_speed)
    print('saturation:', camera.saturation)

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
