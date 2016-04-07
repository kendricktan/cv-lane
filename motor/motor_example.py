from controllers import *
import time

# If you wanna use Pin 20 e.g.
# mainMotor = MotorController(GPIO_no=20)
mainMotor = MotorController() # Using default Pin 16
mainServo = ServoController() # Using default Pin 12

# Motor values are in range -100 <= x <= 100
mainMotor.run_speed(40)

# Servo values are in range 0 <= x <= 100
mainServo.turn_left(50)

time.sleep(1)

mainMotor.stop()

time.sleep(1)

mainMotor.run_speed(-40)
mainServo.turn_left(100)

time.sleep(1)

mainMotor.stop()
mainServo.straighten()
