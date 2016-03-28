import cv2
import numpy as np

class LaneBox:
    def __init__(self):
        self.leftlane_top_xy = (0, 0)
        self.leftlane_middle_xy = (0, 0)
        self.leftlane_bottom_xy = (0, 0)
        self.rightlane_top_xy = (0, 0)
        self.rightlane_middle_xy = (0, 0)
        self.rightlane_bottom_xy = (0, 0)

    def self_print(self):
        print('leftlane_top_xy: %s, leftlane-leftlane_middle_xy: %s, leftlane_bottom_xy: %s\nrightlane_top_xy: %s, rightline_middle_xy: %s, rightlane_bottom_xy: %s'.format(self.leftlane_top_xy, self.leftlane_middle_xy, self.leftlane_bottom_xy, self.rightlane_top_xy, self.rightlane_bottom_xy, self.rightlane_bottom_xy))

# Threshold Settings
BLUE_HSV_RANGE = [([110, 230, 230], [130, 255, 255])]
YELLOW_HSV_RANGE = [([25, 230, 230], [50, 255, 255])]

# Get and read img data
img_name = '../img/highway.jpg'
img = cv2.imread(img_name)
height, width, channels = img.shape
height_dif = int(height/3)
width_dif = int(width/4)

# Crop img and convert to hsv
img_roi = img[int(height/3):int(height*2/3), int(width/4):int(width*3/4)]
img_roi_hsv = cv2.cvtColor(img_roi, cv2.COLOR_BGR2HSV)
roi_height, roi_width, roi_channels = img_roi.shape

# Blue and yellow line filter
for (lower, upper) in BLUE_HSV_RANGE:
    lower = np.array(lower, dtype='uint8')
    upper = np.array(upper, dtype='uint8')

    mask = cv2.inRange(img_roi_hsv, lower, upper)
    ROI_blue = cv2.bitwise_and(img_roi_hsv, img_roi_hsv, mask=mask)

for (lower, upper) in YELLOW_HSV_RANGE:
    lower = np.array(lower, dtype='uint8')
    upper = np.array(upper, dtype='uint8')

    mask = cv2.inRange(img_roi_hsv, lower, upper)
    ROI_yellow = cv2.bitwise_and(img_roi_hsv, img_roi_hsv, mask=mask)

# Simple thresholding and smoothening (to remove noise)
ROI_blue = cv2.medianBlur(ROI_blue, 5)
ROI_blue = cv2.cvtColor(ROI_blue, cv2.COLOR_BGR2GRAY)
ROI_blue, thres_blue = cv2.threshold(ROI_blue, 127, 255, cv2.THRESH_BINARY)

ROI_yellow = cv2.medianBlur(ROI_yellow, 5)
ROI_yellow = cv2.cvtColor(ROI_yellow, cv2.COLOR_BGR2GRAY)
ROI_yellow, thres_yellow = cv2.threshold(ROI_yellow, 127, 255, cv2.THRESH_BINARY)

# LaneBox (points for the lane)
laneBox = LaneBox()

# Detect contours
ROI_thres_list = [thres_blue, thres_yellow]
for thres in ROI_thres_list:

    _, contours, hierarchy = cv2.findContours(thres.copy(),cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Get index of largest contour
    areas = [cv2.contourArea(c) for c in contours]
    max_index = np.argmax(areas)
    cnt = contours[max_index]

    # Metadata of contour
    x, y, w, h = cv2.boundingRect(cnt)

    cv2.circle(img, (width_dif+x+w/2, height_dif+y+h/2), w/2, (0, 0, 255), 2)

# Display img
cv2.imshow('img', img)
#cv2.imshow('img blue', thres_blue)
#cv2.imshow('img yellow', thres_yellow)
cv2.waitKey(0)
cv2.destroyAllWindows()
