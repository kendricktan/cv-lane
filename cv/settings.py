# Camera parameters
AWB_MODE = 'off' # auto white balance
AWB_GAINS = (1.65, 1.4)
EXPOSURE = 'sports'
SHUTTER = 35000 # 0.035 seconds (measured in microseconds)
CAMERA_WIDTH = 320
CAMERA_HEIGHT = 240

# Thresholding parameters
BLUE_HSV_RANGE = [([110, 230, 230], [130, 255, 255])]
YELLOW_HSV_RANGE = [([25, 230, 230], [50, 255, 255])]
HEIGHT_PADDING = int(CAMERA_HEIGHT/3)
WIDTH_PADDING = int(CAMERA_WIDTH/4)
