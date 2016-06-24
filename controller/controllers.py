import os

class MotorController():
    # Speed for our motors
    # range = 0 <= x <= 100
    #
    # motor-dir: 0 = forward, 1 = backwards
    def __init__(self, ser, min_threshold=0, max_threshold=100, is_backwards=False):
        # Our serial to communicate with arduino
        self.ser = ser

        # Some parameters
        self.min_threshold = min_threshold
        self.max_threshold = max_threshold
        self.is_backwards = is_backwards

    # Runs motors
    def run_speed(self, speed):
        if speed <= self.min_threshold:
            speed = self.min_threshold
        elif speed >= self.max_threshold:
            speed = self.max_threshold

        self.ser.write('motor,' + str(speed) + '\n')

    # Toggles direction
    def toggle_dir(self):
        self.is_backwards = not self.is_backwards
        self.ser.write('motor-dir,' + str(int(self.is_backwards)) + '\n')

    # Stop
    def stop(self):
        self.ser.write('motor,0\n')


class ServoController():
    # Servo controlling steering
    # range = 50 <= x <= 150
    # 50 = full right, 150 = full left
    def __init__(self, ser, min_threshold=50, max_threshold=150):
        self.ser = ser

        # Some parameters
        self.min_threshold = min_threshold
        self.max_threshold = max_threshold

    # Turns
    def turn(self, val):
        if val <= self.min_threshold:
            val = self.min_threshold
        elif val >= self.max_threshold:
            val = self.max_threshold

        self.ser.write('steer,' + str(val) + '\n')

    # Straigthens servo
    def straighten(self):
        self.ser.write('steer,50\n')

