# Camera parameters
AWB_MODE = 'off' # auto white balance
AWB_GAINS = (1.65, 2.30)
SATURATION = -5 # If too yellow/green adjust this
EXPOSURE_MODE = 'sports'
EXPOSURE_COMPENSATION = 10
SHUTTER = 0 # measured in microseconds
VIDEO_STABALIZATION = True
ROTATION = 0
CAMERA_WIDTH = 720
CAMERA_HEIGHT = 240
ISO = 0
CONTRAST = 0
BRIGHTNESS = 50
PROP_FORMAT = 1

# Thresholding parameters
BLUE_HSV_RANGE = [([100, 15, 140], [135, 50, 180])] #[([30, 30, 60], [80, 80, 90])]
YELLOW_HSV_RANGE = [([100, 15, 140], [135, 50, 180])]  #[([25, 230, 230], [50, 255, 255])]
HEIGHT_PADDING = int(CAMERA_HEIGHT/2)
WIDTH_PADDING = 0

REGIONS_KEYS = ['top', 'middle', 'bottom']

FRAMES = 65 #How many frames to do CV for (runs at ~37 FPS on pi 2)
