from controllers import *
import time

# If you wanna use Pin 20 e.g.
# mainMotor = MotorController(GPIO_no=20)
mainMotor = MotorController() # Using default Pin 16

# Motor values are in range -100 <= x <= 100
mainMotor.run_speed(40)

time.sleep(1)

mainMotor.stop()

time.sleep(1)

mainMotor.run_speed(-40)

time.sleep(1)

mainMotor.stop()
