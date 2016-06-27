import os
import serial

class Controller():
    def __init__(self, is_motor_forwards=True):
        # Our serial to communicate with arduino
        self.ser = serial.Serial('/dev/ttyUSB0', 57600)
        self.is_motor_forwards = is_motor_forwards

        self.run_speed(0)
        self.ser.write('motor-dir,' + str(int(is_motor_forwards)) + '\n')

    #### Motors ####
    # range = 0 <= x <= 100
    #
    # motor-dir: 0 = forward, 1 = backwards
    # Runs motors
    def run_speed(self, speed):
        if speed < 0:
            speed = 0
        elif speed > 100:
            speed = 100

        self.ser.write('motor,' + str(speed) + '\n')

    # Toggles direction
    def toggle_dir(self):
        self.is_motor_forwards = not self.is_motor_forwards
        self.ser.write('motor-dir,' + str(int(self.is_motor_forwards)) + '\n')

    # Stop
    def stop(self):
        self.ser.write('motor,0\n')

    ##### Servo testing ####
    # Turns
    # range = 50 <= x <= 150
    # 50 = full right, 150 = full left
    def turn(self, val, left=False, right=False):

        if left:
            val = 100 + int(abs(val))
        elif right:
            val = 100 - int(abs(val))

        if val < 50:
            val = 50
        elif val > 150:
            val = 150

        self.ser.write('steer,' + str(val) + '\n')

    # Turning for PID
    def pid_turn(self, val, left=False, right=False):
        self.turn(50*val, left=left, right=right)

    # Straigthens servo
    def straighten(self):
        self.ser.write('steer,100\n')

