import os


class BlastGPIO(object):
    # GPIO pin used to echo into /dev/servoblaster
    #
    # e.g. echo P1-GPIO_no=x > /dev/servoblaster
    def __init__(self, GPIO_no, min_threshold=1000, max_threshold=2000):
        self.GPIO_no = GPIO_no

        # Thresholding for outputs
        self.min_threshold = min_threshold
        self.max_threshold = max_threshold

        # Neutral value
        self.neutral_val = int((self.max_threshold + self.min_threshold) / 2)

    # Blast value into port
    def blast_value(self, val):
        os.system('echo P1-' + str(self.GPIO_no) + '=' + str(val) + 'us > /dev/servoblaster')

    # Puts it into neutral mode
    def blast_neutral(self):
        n = str(int((self.max_threshold + self.min_threshold) / 2))
        os.system('echo P1-' + str(self.GPIO_no) + '=' + n + 'us > /dev/servoblaster')

    # Gets the neutral value
    def get_neutral_val(self):
        return self.neutral_val


class MotorController(BlastGPIO):
    # Speed for our motors
    # range = -100 <= x <= 100
    # negative value = reverse
    def __init__(self, GPIO_no=16, min_threshold=1000, max_threshold=2000, speed=0):
        super(self.__class__, self).__init__(GPIO_no, min_threshold, max_threshold)
        self.speed = speed

    # Runs motors
    def run(self):
        speed_val = super(self.__class__, self).get_neutral_val()
        speed_val += 5 * self.speed
        super(self.__class__, self).blast_value(speed_val)

    def run_speed(self, speed):
        self.speed = speed
        self.run()

    # Stop
    def stop(self):
        super(self.__class__, self).blast_neutral()


class ServoController(BlastGPIO):
    def __init__(self, GPIO_no=12, min_threshold=1000, max_threshold=2000, angle=0):
        super(self.__class__, self).__init__(GPIO_no, min_threshold, max_threshold)
        self.angle = angle
        self.toggle_val = 1

    # Toggles direction for turning left and right
    # ONLY use this if turn_left turns right
    def toggle_dir(self):
        self.toggle_val = -self.toggle_val

    # Turns
    def turn(self, isLeft):
        turn_val = super(self.__class__, self).get_neutral_val()
        if isLeft:
            turn_val += (5 * self.value * self.toggle_val)
        else:
            turn_val -= (5 * self.value * self.toggle_val)
        super(self.__class__, self).blast_value(turn_val)

    # Turns left
    # value range is between 0-100
    # larger the value, the greater the angle of turn
    def turn_left(self, value):
        self.value = value
        self.turn(True)

    # Turns right
    # value range is between 0-100
    # larger the value, the greater the angle of turning
    def turn_right(self, value):
        self.value = value
        self.turn(False)

    # Straigthens servo
    def straighten(self):
        super(self.__class__, self).blast_neutral()
