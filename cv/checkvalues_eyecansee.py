from EyeCanSee import *

camera = EyeCanSee(debug=True, key_to_continue=False)

while True:
    camera.where_lane_be()

#camera.calculate_fps()
