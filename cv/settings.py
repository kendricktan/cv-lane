# Camera parameters
AWB_MODE = 'off' # auto white balance
AWB_GAINS = (1.65, 2.30)
SATURATION = -5 # If too yellow/green adjust this
EXPOSURE_MODE = 'sports'
EXPOSURE_COMPENSATION = 10
SHUTTER = 1985 # measured in microseconds
VIDEO_STABALIZATION = True
ROTATION = 0
CAMERA_WIDTH = 720
CAMERA_HEIGHT = 240
ISO = 800
CONTRAST = 50
BRIGHTNESS = 75
PROP_FORMAT = 1

# Thresholding parameters
# Red Elec Tape BLUE_HSV_RANGE = [([0, 80, 100], [15, 120, 130])] #[([30, 30, 60], [80, 80, 90])]
# Red Elec Tape YELLOW_HSV_RANGE = [([0, 80, 100], [15, 120, 130])]  #[([25, 230, 230], [50, 255, 255])]

BLUE_HSV_RANGE = [([100, 15, 140], [135, 50, 180])] #[([30, 30, 60], [80, 80, 90])]
YELLOW_HSV_RANGE = [([100, 15, 140], [135, 50, 180])]  #[([25, 230, 230], [50, 255, 255])]
HEIGHT_PADDING = int(CAMERA_HEIGHT/2)
WIDTH_PADDING = 0#int(CAMERA_WIDTH/4)

REGIONS_KEYS = ['top', 'middle', 'bottom']

FRAMES = 65 #How many frames to do CV for (runs at ~37 FPS on pi 2)
