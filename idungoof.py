from controller.controllers import Controller
import time

car_controller = Controller()

time.sleep(0.5)

car_controller.stop()
car_controller.straighten()
