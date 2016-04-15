from EyeCanSee import *

camera = EyeCanSee(debug=True, is_usb_webcam=True)

while True:
    camera.where_lane_be()

#camera.calculate_fps()
