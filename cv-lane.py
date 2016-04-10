from cv.EyeCanSee import *
from ai.pid import *
from ai.KalmanFilter import *
from controller.controllers import *

import cv2
import math
import time
import cv.settings

# Our class instances
camera = EyeCanSee()

# Kalman filter
measurement_standard_deviation = 0
process_variance = 15
estimated_measurement_variance = measurement_standard_deviation ** 2  # 0.05 ** 2
kalman_filter = {}

# previous values (in case can't detect line)
# we'll go and continue previous location
previous_values = {}

# PID for each region (if we do decide to add any)
p_ = {'top': 0.122, 'middle': 0.05, 'bottom': 0.065}
i_ = {'top': 0.022, 'middle': 0.031, 'bottom': 0.04}
d_ = {'top': 0.1, 'middle': 0.1, 'bottom': 0.12}
pid = {}

for region in settings.REGIONS_KEYS:
    pid[region] = PID(p=p_[region], i=i_[region], d=d_[region], integrator_max=50, integrator_min=-50)
    previous_values[region] = 0.0
    kalman_filter[region] = KalmanFilter(process_variance, estimated_measurement_variance)


# Controllers
motor = MotorController() # values: -100 <= x <= 100
steering = ServoController() # values: 0 <= x <= 100

motor.run_speed(20)

for i in range(0, 125):
    # Trys and get our lane
    camera.where_lane_be()

    # Pid on each region
    total_pid = 0
    for region in camera.relative_error:
        # If it detects lane, then use that region, otherwise
        # use previous value
        if camera.detected_lane[region]:
            # Filters out irregular values
            kalman_filter[region].input_latest_noisy_measurement(camera.relative_error[region])
            filtered_value = kalman_filter[region].get_latest_estimated_measurement()

            # Add pid to previous value and total_pid value
            previous_values[region] = filtered_value
            total_pid += pid[region].update(filtered_value)
        else:
            total_pid += previous_values[region]

    # Negative total_pid = need to turn left
    # Positive total_pid = need to turn right
    # Try to keep pid 0
    if total_pid < 0:
        if total_pid < -100:
            total_pid = -100
        steering.turn_left(abs(total_pid))

    elif total_pid > 0:
        if total_pid > 100:
            total_pid = 100
        steering.turn_right(abs(total_pid))

    time.sleep(0.01)

steering.straighten()
motor.stop()
