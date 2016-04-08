from cv.EyeCanSee import *
from ai.pid import *
from controller.controllers import *

import cv2
import math
import time
import cv.settings

# Our class instances
camera = EyeCanSee()

# PID for each region (if we do decide to add any)
pid = {}
for region in settings.REGIONS_KEYS:
    pid[region] = PID()

motor = MotorController() # values: -100 <= x <= 100
steering = ServoController() # values: 0 <= x <= 100

motor.run_speed(10)

for i in range(0, 5):
    # Trys and get our lane
    camera.where_lane_be()

    # Pid on each region
    total_pid = 0
    for region in camera.relative_error:
        total_pid += pid[region].update(camera.relative_error[region])
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

motor.stop()
