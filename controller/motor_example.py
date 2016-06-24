from controllers import *
import time
import serial

# Our communication to arduino
ser = serial.Serial('/dev/ttyUSB0', 9600)

mainMotor = MotorController(ser)

# Motor values are in range 0 <= x <= 100
mainMotor.run_speed(30)

time.sleep(1)

mainMotor.stop()

time.sleep(1)

mainMotor.toggle_dir()

mainMotor.run_speed(30)

time.sleep(1)

mainMotor.stop()
