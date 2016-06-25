# Lane detection using opencv

# This communicates with Jabelone's [car-controller](https://github.com/jabelone/car-controller/)

Basic Usage:

1) Switch connected to pin 11 and ground.  LED on pin 40 with appropriate resistor.

2) Pi Camera connected, facing right way up, pointed almost straight down at front.

3) Run cv/get_hsv.py and double click on a few points along the line.  Take a point below the lowest for each H, S and V.  Take a point above the highest, you now have a range.  Modify the settings file entry and enter the new range for either colour.

4) Run cv/get_check_hsv_values.py and press space to refresh the image.  When you move the camera it should track the line.

5) Run cv-lane.py.  The LED should turn on for a few seconds then start flashing.  Once it starts flashing flick the switch to start the CV.  Flick the switch again to pause while it's running.

Currently it is configured to follow a single line.
