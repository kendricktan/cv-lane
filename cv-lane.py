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

output = commands.getoutput('ps -A')

if 'servod' in output:
    print("Servo Blaster process found.")
else:
    print("Servo Blaster process not found. Starting it now.")
    os.system("echo terminator | sudo service servoblaster start")

# Our class instances
camera = EyeCanSee()

# Kalman filter
kalman_filter = KalmanFilter(aisettings.VAR, aisettings.EST_VAR)

# previous values (in case can't detect line)
# we'll go and continue previous location
previous_value_ = 0.0

# PID for each region (if we do decide to add any)
pid = PID(p=aisettings.P_, i=aisettings.I_, d=aisettings.D_)

# Controllers
motor = MotorController()  # values: -100 <= x <= 100
steering = ServoController()  # values: 0 <= x <= 100

motor.stop()
steering.straighten()

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

def status():
    global t
    sys.stdout.write('\r')
    sys.stdout.write(" ")
    sys.stdout.flush()
    t = threading.Timer(1, status).start()

status()  # Start the first "thread" for blinking dot
time.sleep(0.5)  # Leave a 0.5 second delay so it alternates (ie blinks)


def status2():
    global t2
    sys.stdout.write('\r')
    sys.stdout.write(".")
    sys.stdout.flush()
    t2 = threading.Timer(1, status2).start()


status2()  # start the second "thread" for blinking dot

# Start moving forward
motor.run_speed(35)

for i in range(0, cvsettings.FRAMES):  # For the amount of frames we want CV on
    while (GPIO.input(11) == 1):
        motor.stop()  # Reset throttle
        steering.straighten()  # Reset steering

    # Trys and get our lane
    camera.where_lane_be()

    total_pid = 0

    # If it detects lane, then proceed, otherwise use previous region
    if camera.detected_lane:
        # Filters out irregular values
        kalman_filter.input_latest_noisy_measurement(camera.relative_error)
        filtered_value = kalman_filter.get_latest_estimated_measurement()

        # Add pid to previous value and total_pid value
        previous_values = filtered_value
        total_pid += pid.update(filtered_value)

    else:
        total_pid += previous_values

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

    # Motors slow down around bends
    motor_speed = map_func(abs(total_pid), 0, 100, 20, 35)
    motor.run_speed(motor_speed)

    time.sleep(0.01)

# Turn everything off now that we're done and exit the program
steering.straighten()
motor.stop()

# LED
GPIO.output(40, 0)
print("Finished running CV.  Now exiting the program.")

# Kill the threads from the blinking dot
os.system('kill $PPID')
