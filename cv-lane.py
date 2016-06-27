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

# Our class instances
camera = EyeCanSee()

# Kalman filter
kalman_filter = KalmanFilter(aisettings.VAR, aisettings.EST_VAR)
#kalman_filter.input_latest_noisy_measurement(0)

# PID for each region (if we do decide to add any)
pid = PID(
    p=aisettings.P_,
    i=aisettings.I_,
    d=aisettings.D_,
    min_threshold=aisettings.PID_MIN_VAL,
    max_threshold=aisettings.PID_MAX_VAL
)
#pid.update(0)

# Controllers
car_controller = Controller()
car_controller.stop()
car_controller.straighten()

# Wait for the switch to be "armed" before starting
# (and blink the LED rapidly so we know)
print("Initialisation complete.")

raw_input("Please press any key to start driving *immediately*")
print("Starting autonomous control now!")


#for i in range(0, cvsettings.FRAMES):  # For the amount of frames we want CV on
while True:
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
        car_controller.pid_turn(calibrated_value, left=True)

    elif filtered_value > 0:
        car_controller.pid_turn(calibrated_value, right=True)

    # Doesn't work without sleep 0.03 or more for some reason...
    car_controller.run_speed(35)

# Turn everything off now that we're done and exit the program
car_controller.straighten()
car_controller.stop()

# LED
print("Finished running CV.  Now exiting the program.")
