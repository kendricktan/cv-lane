from controllers import *
import time
import serial

ser = serial.Serial('/dev/ttyUSB0', 9600)

mainServo = ServoController(ser)

time.sleep(1)

mainServo.turn(150)

time.sleep(1)

mainServo.turn(50)

time.sleep(1)

mainServo.straighten()
