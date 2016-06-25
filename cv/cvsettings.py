# Camera parameters
AWB_MODE = 'off'
# AWB_MODE choices: 'off','auto','sunlight','cloudy','shade','tungsten','fluorescent','incandescent','flash','horizon'
EXPOSURE_MODE = 'off'
# Exposure mode choices: 'off','auto','night','nightpreview','backlight','spotlight','sports','snow','beach','verylong','fixedfps','antishake','fireworks'

AWB_GAINS = (1.31, 1.37)  # Run get_camera_settings to find these values
SATURATION = 0  # If too yellow/green adjust this
EXPOSURE_COMPENSATION = 0
SHUTTER = 75000  # measured in picoseconds?
VIDEO_STABALIZATION = True
ROTATION = 0
CAMERA_WIDTH = 1088
CAMERA_HEIGHT = 480
ISO = 0
CONTRAST = 0
BRIGHTNESS = 50
PROP_FORMAT = 1

# Thresholding parameters
BLUE_HSV_RANGE = [([45, 100, 10], [65, 255, 35])]  # [([30, 30, 60], [80, 80, 90])]
YELLOW_HSV_RANGE = [([25, 200, 80], [50, 255, 100])]  # [([25, 230, 230], [50, 255, 255])]

HEIGHT_PADDING_BOTTOM = int(CAMERA_HEIGHT / 1.55) # Where the bottom image ROI is gonna ba
HEIGHT_PADDING_TOP = int(CAMERA_HEIGHT / 2) # Where the top image ROI is gonna be

WIDTH_PADDING = 0

IMG_ROI_HEIGHT = 20

FRAMES = 65  # How many frames to do CV for
