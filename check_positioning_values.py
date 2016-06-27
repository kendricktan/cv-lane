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

# Our class instances
camera = EyeCanSee()

# Kalman filter
kalman_filter = KalmanFilter(aisettings.VAR, aisettings.EST_VAR)
kalman_filter.input_latest_noisy_measurement(0)

# previous values (in case can't detect line)
# we'll go and continue previous location
previous_values = 0.0

# PID for each region (if we do decide to add any)
pid = PID(
    p=aisettings.P_,
    i=aisettings.I_,
    d=aisettings.D_,
    min_threshold=aisettings.PID_MIN_VAL,
    max_threshold=aisettings.PID_MAX_VAL
)
pid.update(0)

for i in range(0, 5):  # For the amount of frames we want CV on
    # Trys and get our lane
    camera.where_lane_be()

    # Filters out irregular values
    kalman_filter.input_latest_noisy_measurement(camera.relative_error)
    filtered_value = kalman_filter.get_latest_estimated_measurement()

    # Add pid to previous value and total_pid value
    calibrated_value = pid.update(filtered_value)

    # Negative total_pid = need to turn left
    # Positive total_pid = need to turn right
    # Try to keep pid 0

    print('Is lane detected: %s' % str(camera.detected_lane))
    print('Camera relative error: %s'% camera.relative_error)
    print('Filtered value: %s'% filtered_value)

    if filtered_value < 0:
        print('Left force: %s' % (calibrated_value*50.0))

    elif filtered_value > 0:
        print('Right force: %s' % (calibrated_value*50.0))

    print('----')

    time.sleep(0.05)
