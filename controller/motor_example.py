from controllers import *
import time

car_controller = Controller()

# Motor values are in range 0 <= x <= 100
for i in range(0, 10):
    car_controller.run_speed(10*i)
    time.sleep(0.5)

car_controller.toggle_dir()
car_controller.run_speed(50)
time.sleep(2)

car_controller.stop()
