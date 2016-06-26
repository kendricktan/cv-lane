from EyeCanSee import *

camera = EyeCanSee(debug=True)

while True:
    camera.where_lane_be()
    camera.where_object_be()

# camera.calculate_fps()
