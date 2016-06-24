# Camera parameters
AWB_MODE = 'auto'
# AWB_MODE choices: 'off','auto','sunlight','cloudy','shade','tungsten','fluorescent','incandescent','flash','horizon'
EXPOSURE_MODE = 'auto'
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
BLUE_HSV_RANGE = [([35, 100, 60], [55, 180, 120])]  # [([30, 30, 60], [80, 80, 90])]
YELLOW_HSV_RANGE = [([25, 140, 190], [50, 220, 230])]  # [([25, 230, 230], [50, 255, 255])]
HEIGHT_PADDING = int(CAMERA_HEIGHT / 1.5)
WIDTH_PADDING = 0

REGIONS_KEYS = ['middle']  # ['top', 'middle', 'bottom']

FRAMES = 65 # How many frames to do CV for (runs at ~37 FPS on pi 2)
