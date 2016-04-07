import cv2
import numpy as np
from settings import *

# Get and read img data
img_name = '../img/highway.jpg'
img = cv2.imread(img_name)
height, width, channels = img.shape
height_dif = int(height/3)
width_dif = int(width/4)


# Crop img and convert to hsv
img_roi = img[HEIGHT_PADDING:HEIGHT_PADDING*2, WIDTH_PADDING:int(WIDTH_PADDING*3)]
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

# Split contours into 3 sections: top, middle, and bottom
thres_yellow_dict = {'top': thres_yellow[:int(roi_height/3), :], 'middle': thres_yellow[int(roi_height/3):int(roi_height*2/3), :], 'bottom': thres_yellow[int(roi_height*2/3):,]}
thres_blue_dict = {'top': thres_blue[:int(roi_height/3), :], 'middle': thres_blue[int(roi_height/3):int(roi_height*2/3), :], 'bottom': thres_blue[int(roi_height*2/3):,]}

# Metadata (x,y,w,h)for our ROI
contour_metadata = {}
for cur_thres_dict in [thres_yellow_dict, thres_blue_dict]:
    if cur_thres_dict is thres_yellow_dict:
        temp_ = 'yellow_'
    else:
        temp_ = 'blue_'

    for key in cur_thres_dict:
        # Gets image from dict
        cur_img = cur_thres_dict[key]
        _, contours, hierarchy = cv2.findContours(cur_img.copy(),cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        cur_height, cur_width = cur_img.shape

        temp_key = temp_ + key
        # Get index of largest contour
        try:
            areas = [cv2.contourArea(c) for c in contours]
            max_index = np.argmax(areas)
            cnt = contours[max_index]

            # Metadata of contour
            x, y, w, h = cv2.boundingRect(cnt)

            # Normalize it to the original picture
            if key == 'middle':
                y += int(roi_height/3)
            elif key == 'bottom':
                y += int(roi_height*2/3)

            x += int(WIDTH_PADDING+w/2)
            y += int(HEIGHT_PADDING+h/2)

            contour_metadata[temp_key] = (x, y)

            cv2.circle(img, (x, y), 5, (0, 0, 255), 2)

        # If it throws an error then it doesn't have a ROI
        # Means we're too far off to the left or right
        except:
            # Blue is left lane, Yellow is right lane
            x = int(WIDTH_PADDING+cur_width/2)
            y = int(cur_height/2) + int(HEIGHT_PADDING+cur_height/2)

            if 'yellow' in temp_:
                x += int(cur_width)

            if key == 'middle':
                y += int(roi_height/3)
            elif key == 'bottom':
                y += int(roi_height*2/3)

            contour_metadata[temp_key] = (x, y)
            cv2.circle(img, (x, y), 5, (0, 0, 255), 2)

REGIONS_KEYS = ['top', 'middle', 'bottom']

# Gets centered location for each region
centered_coord = {}
for REGION in REGIONS_KEYS:
    left_xy = contour_metadata['blue_' + REGION]
    right_xy = contour_metadata['yellow_' + REGION]
    added_xy =(left_xy[0]+right_xy[0], left_xy[1]+right_xy[1])
    centered_coord[REGION] = (int(added_xy[0]/2), int(added_xy[1]/2))
    cv2.circle(img, centered_coord[REGION], 5, (0, 255, 0), 3)

# Display lines
cv2.line(img, centered_coord['top'], centered_coord['middle'], (255, 0, 0), 2)
cv2.line(img, centered_coord['middle'], centered_coord['bottom'], (255, 0, 0), 2)

cv2.line(img, contour_metadata['yellow_top'], contour_metadata['yellow_middle'], (0, 0, 255), 2)
cv2.line(img, contour_metadata['yellow_middle'], contour_metadata['yellow_bottom'], (0, 0, 255), 2)
cv2.line(img, contour_metadata['blue_top'], contour_metadata['blue_middle'], (0, 0, 255), 2)
cv2.line(img, contour_metadata['blue_middle'], contour_metadata['blue_bottom'], (0, 0, 255), 2)

# Display img
cv2.imshow('img', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
