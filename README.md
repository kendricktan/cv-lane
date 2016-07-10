# Lane detection using opencv

![](http://i.makeagif.com/media/7-10-2016/UpemdQ.gif)

### This communicates with Jabelone's [car-controller](https://github.com/jabelone/car-controller/)
Jabelone's car-controller is used to output the pwm signals to the steering servo and motor controller.  Read the set-up instructions for car-controller for wiring instructions.  Plug the car-controller arduino into the pi via USB so cv-lane can talk to it.

# Basic Usage:

1) A hardware safety switch is connected between pin 11 and ground.  There is an LED between pin 40 and ground with an appropriate resistor.

2) A Pi camera is connected and it's facing the right way up, angled down a bit. (optimum angle/placement depends on your setup)

3) Run cv/get_hsv.py and double click on a few points along the line.  Take a point below the lowest for each H, S and V.  Take a point above the highest, you now have a range.  Modify the settings file entry and enter the new range for either colour.

4) Run cv/get_check_hsv_values.py and press space to refresh the image.  When you move the camera it should track the line.

5) Run cv-lane.py.  The LED should turn on for a few seconds wile initialising and then start flashing.  Once it starts flashing press any key when prompted to *immediately* start moving forward.  Ensure the hardware safety switch is on or cv-lane will not run.  You may flick the switch off to pause while it's running.
