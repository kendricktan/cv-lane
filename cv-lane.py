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
import controller.controllersettings as ctlsettings

print("Initialising...")

GPIO.setmode(GPIO.BOARD)  # Required to setup the naming convention
GPIO.setwarnings(False)  # Ignore annoying warnings
GPIO.setup(11, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Arming pin is input
GPIO.setup(40, GPIO.OUT)  # LED pin is output
GPIO.output(40, 1)  # Set LED pin to "high" or on

# Our class instances
camera = EyeCanSee()

# Kalman filter
kalman_filter = KalmanFilter(aisettings.VAR, aisettings.EST_VAR)

# previous values (in case can't detect line)
# we'll go and continue previous location
previous_values = 0.0

# PID for each region (if we do decide to add any)
pid = PID(
    p=aisettings.P_,
    i=aisettings.I_,
    d=aisettings.D_,
    min_threshold=ctlsettings.PID_MIN_VAL,
    max_threshold=ctlsettings.PID_MAX_VAL
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
    GPIO.output(40, 1)
    time.sleep(0.1)
    GPIO.output(40, 0)
    time.sleep(0.25)

for i in range(0, 5):
    GPIO.output(40, 1)
    time.sleep(0.1)
    GPIO.output(40, 0)
    time.sleep(0.25)

time.sleep(0.5)  # Leave a 0.5 second delay so it alternates (ie blinks)

print('Starting autonomous control now...')

for i in range(0, cvsettings.FRAMES):  # For the amount of frames we want CV on
    while (GPIO.input(11) == 1):
        car_controller.stop()  # Reset throttle
        car_controller.straighten()  # Reset steering

    # Trys and get our lane
    camera.where_lane_be()

    total_pid = 0

    # If it detects lane, then proceed, otherwise use previous region
    if camera.detected_lane:
        # Filters out irregular values
        kalman_filter.input_latest_noisy_measurement(camera.relative_error)
        filtered_value = kalman_filter.get_latest_estimated_measurement()

        # Add pid to previous value and total_pid value
        total_pid += pid.update(filtered_value)
        previous_values = total_pid

    else:
        total_pid += previous_values

    # Negative total_pid = need to turn left
    # Positive total_pid = need to turn right
    # Try to keep pid 0
    steer_val = map_func(total_pid, ctlsettings.PID_MIN_VAL, ctlsettings.PID_MAX_VAL, 0.0, 50.0) # 50 because 50 <= x <= 150 (100 is neutral)
    if total_pid < 0:
        #print('Left: %s' % total_pid)
        car_controller.turn(abs(steer_val), left=True)

    elif total_pid > 0:
        #print('Right: %s' % total_pid)
        car_controller.turn(abs(steer_val), left=False)

    # Motors slow down around bends
    #motor_speed = map_func(abs(total_pid), -3.0, 3.0, 60.0, 75.0)
    car_controller.run_speed(40)

    time.sleep(0.05)

# Turn everything off now that we're done and exit the program
car_controller.straighten()
car_controller.stop()

# LED
GPIO.output(40, 0)
print("Finished running CV.  Now exiting the program.")

