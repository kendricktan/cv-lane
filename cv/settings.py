# Camera parameters
AWB_MODE = 'fluorescent'
# AWB_MODE choices: 'off','auto','sunlight','cloudy','shade','tungsten','fluorescent','incandescent','flash','horizon'
EXPOSURE_MODE = 'sports'
# Exposure mode choices: 'off','auto','night','nightpreview','backlight','spotlight','sports','snow','beach','verylong','fixedfps','antishake','fireworks'

AWB_GAINS = (1.40, 1.90)
SATURATION = 0  # If too yellow/green adjust this
EXPOSURE_COMPENSATION = 0
SHUTTER = 0  # measured in microseconds
VIDEO_STABALIZATION = True
ROTATION = 0
CAMERA_WIDTH = 720
CAMERA_HEIGHT = 480
ISO = 0
CONTRAST = 0
BRIGHTNESS = 50
PROP_FORMAT = 1

# Thresholding parameters
BLUE_HSV_RANGE = [([0, 255, 0], [0, 255, 25])]  # [([30, 30, 60], [80, 80, 90])]
YELLOW_HSV_RANGE = [([10, 220, 100], [20, 255, 140])]  # [([25, 230, 230], [50, 255, 255])]
HEIGHT_PADDING = int(CAMERA_HEIGHT / 2)
WIDTH_PADDING = 0

REGIONS_KEYS = ['middle']  # ['top', 'middle', 'bottom']

FRAMES = 65  # How many frames to do CV for (runs at ~37 FPS on pi 2)
