from cv.EyeCanSee import *
from ai.pid import *
from ai.KalmanFilter import *
from controller.controllers import *
from etc.etc import * # The etc functions dumped into there

import RPi.GPIO as GPIO  # Import the GPIO library
import time
import commands
import os
import sys
import threading
import ai.aisettings as aisettings
import cv.cvsettings as cvsettings

print("Initialising...")

GPIO.setmode(GPIO.BOARD)  # Required to setup the naming convention
GPIO.setwarnings(False)  # Ignore annoying warnings
GPIO.setup(11, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Arming pin is input
GPIO.setup(40, GPIO.OUT)  # LED pin is output
GPIO.output(40, 1)  # Set LED pin to "high" or on

# Blinks LED (hardcoded to GPIO 40)
def blink():
    GPIO.output(40, 1)
    time.sleep(0.1)
    GPIO.output(40, 0)
    time.sleep(0.25)

# Our class instances
camera = EyeCanSee()

# Kalman filter
kalman_filter = KalmanFilter(aisettings.VAR, aisettings.EST_VAR)

# PID for each region (if we do decide to add any)
pid = PID(
    p=aisettings.P_,
    i=aisettings.I_,
    d=aisettings.D_,
    min_threshold=aisettings.PID_MIN_VAL,
    max_threshold=aisettings.PID_MAX_VAL
)

# Controllers
car_controller = Controller()
car_controller.stop()
car_controller.straighten()

# Wait for the switch to be "armed" before starting
# (and blink the LED rapidly so we know)
print("Initialisation complete.")

if (GPIO.input(11) == 1):
    print("Start the CV by turning the arming switch on.")

while (GPIO.input(11) == 1):
    blink()

raw_input("Please press any key to start driving *immediately*")
print("Starting autonomous control now!")

for i in range(0, cvsettings.FRAMES):  # For the amount of frames we want CV on
    while (GPIO.input(11) == 1):
        car_controller.stop()  # Reset throttle
        car_controller.straighten()  # Reset steering

    # Trys and get our lane
    camera.where_lane_be()

    # Filters out irregular values
    kalman_filter.input_latest_noisy_measurement(camera.relative_error)
    filtered_value = kalman_filter.get_latest_estimated_measurement()

    # Get pid value (to steer)
    calibrated_value = pid.update(filtered_value)

    # Negative total_pid = need to turn left
    # Positive total_pid = need to turn right
    # Try to keep pid 0

    if filtered_value < 0:
        #print('Left: %s' % total_pid)
        car_controller.turn(calibrated_value, left=True)

    elif filtered_value > 0:
        #print('Right: %s' % total_pid)
        car_controller.turn(calibrated_value, right=True)

    car_controller.run_speed(35)

    # Doesn't work without sleep 0.03 or more for some reason...
    time.sleep(0.03)

# Turn everything off now that we're done and exit the program
car_controller.straighten()
car_controller.stop()

# LED
GPIO.output(40, 0)
print("Finished running CV.  Now exiting the program.")
