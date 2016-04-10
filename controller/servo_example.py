from controllers import *
import time

# If you wanna use Pin 20 e.g.
# mainMotor = MotorController(GPIO_no=20)
mainServo = ServoController() # Using default Pin 12

time.sleep(1)

mainServo.turn_right(100)

time.sleep(1)

mainServo.turn_left(100)
time.sleep(1)
mainServo.straighten()
