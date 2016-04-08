from __future__ import print_function
from imutils.video.pivideostream import PiVideoStream
from imutils.video import FPS
from picamera.array import PiRGBArray
from picamera import PiCamera
import argparse
import imutils
import time
import cv2
import numpy as np
import settings

class EyeCanSee(object):
    def __init__(self, debug=False):
        # Our video stream
        self.vs = PiVideoStream(resolution=(settings.CAMERA_WIDTH, settings.CAMERA_HEIGHT))

        # Camera settings
        self.vs.camera.shutter_speed = settings.SHUTTER
        self.vs.camera.exposure_mode = settings.EXPOSURE_MODE
        self.vs.camera.exposure_compensation = settings.EXPOSURE_COMPENSATION
        self.vs.camera.awb_gains = settings.AWB_GAINS
        self.vs.camera.awb_mode = settings.AWB_MODE
        self.vs.camera.saturation = settings.SATURATION
        self.vs.camera.video_stabilization = settings.VIDEO_STABALIZATION

        # Has camera started
        self.camera_started = False

        self.start_camera() # Starts our camera

        # debug mode on?
        self.debug = debug

    # Starts camera (needs to be called before run)
    def start_camera(self):
        self.camera_started = True
        self.vs.start()
        time.sleep(2.0) # Wait for camera to cool

    def stop_camera(self):
        self.camera_started = False
        self.vs.stop()

    # Grabs frame from camera
    def grab_frame(self):
        # Starts camera if it hasn't been started
        if not self.camera_started:
            self.start_camera()
        self.img = self.vs.read()

    # Normalizes our image
    def normalize_img(self):
        # Crop img and convert to hsv
        self.img_roi = self.img[settings.HEIGHT_PADDING:settings.HEIGHT_PADDING*2, :]
        self.img_roi_hsv = cv2.cvtColor(self.img_roi, cv2.COLOR_BGR2HSV)

        # Get our ROI's shape
        self.roi_height, self.roi_width, self.roi_channels = self.img_roi.shape

    # Smooth image and convert to bianry image (threshold)
    # Filter out colors that are not within the RANGE value
    def filter_smooth_thres(self, RANGE):
        for (lower, upper) in RANGE:
            lower = np.array(lower, dtype='uint8')
            upper = np.array(upper, dtype='uint8')

            mask = cv2.inRange(self.img_roi_hsv, lower, upper)
            ROI_masked = cv2.bitwise_and(self.img_roi_hsv, self.img_roi_hsv, mask=mask)

        ROI_masked = cv2.medianBlur(ROI_masked, 5)
        ROI_masked = cv2.cvtColor(ROI_masked, cv2.COLOR_BGR2GRAY)
        ROI_masked, thres = cv2.threshold(ROI_masked, 127, 255, cv2.THRESH_BINARY)
        return ROI_masked, thres

    # Gets metadata from our contours
    def get_contour_metadata(self):
        # Split contours into 3 sections: top, middle, and bottom
        thres_yellow_dict = {}
        thres_blue_dict = {}
        for REGION in settings.REGIONS_KEYS:
            if REGION == 'top':
                thres_yellow_dict['top'] = self.thres_yellow[:int(self.roi_height/3)]
                thres_blue_dict['top'] = self.thres_blue[:int(self.roi_height/3), :]

            elif REGION == 'middle':
                thres_yellow_dict['middle'] = self.thres_yellow[int(self.roi_height/3):int(self.roi_height*2/3), :]
                thres_blue_dict['middle'] = self.thres_blue[int(self.roi_height/3):int(self.roi_height*2/3), :]

            elif REGION =='bottom':
                thres_yellow_dict['bottom'] = self.thres_yellow[int(self.roi_height*2/3):,]
                thres_blue_dict['bottom'] = self.thres_blue[int(self.roi_height*2/3):,]


        #thres_yellow_dict = {'top': self.thres_yellow[:int(self.roi_height/3), :], 'middle': self.thres_yellow[int(self.roi_height/3):int(self.roi_height*2/3), :], 'bottom': self.thres_yellow[int(self.roi_height*2/3):,]}
        #thres_blue_dict = {'top': self.thres_blue[:int(self.roi_height/3), :], 'middle': self.thres_blue[int(self.roi_height/3):int(self.roi_height*2/3), :], 'bottom': self.thres_blue[int(self.roi_height*2/3):,]}

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
                        y += int(self.roi_height/3)
                    elif key == 'bottom':
                        y += int(self.roi_height*2/3)

                    x += int(settings.WIDTH_PADDING+w/2)
                    y += int(settings.HEIGHT_PADDING+h/2)

                    contour_metadata[temp_key] = (x, y)

                    if self.debug:
                        cv2.circle(self.img, (x, y), 5, (0, 0, 255), 2)

                # If it throws an error then it doesn't have a ROI
                # Means we're too far off to the left or right
                except:
                    # Blue is left lane, Yellow is right lane
                    x = int(settings.WIDTH_PADDING+cur_width/2)
                    y = int(cur_height/2) + int(settings.HEIGHT_PADDING+cur_height/2)

                    if 'yellow' in temp_:
                        x += int(cur_width)

                    if key == 'middle':
                        y += int(self.roi_height/3)
                    elif key == 'bottom':
                        y += int(self.roi_height*2/3)

                    contour_metadata[temp_key] = (x, y)

                    if self.debug:
                        cv2.circle(self.img, (x, y), 5, (0, 0, 255), 2)

        return contour_metadata

    # Gets the centered coord of the detected lines
    def get_centered_coord(self):
        centered_coord = {}
        for REGION in settings.REGIONS_KEYS:
            left_xy = self.contour_metadata['blue_' + REGION]
            right_xy = self.contour_metadata['yellow_' + REGION]
            added_xy =(left_xy[0]+right_xy[0], left_xy[1]+right_xy[1])
            centered_coord[REGION] = (int(added_xy[0]/2), int(added_xy[1]/2))

            if self.debug:
                cv2.circle(self.img, centered_coord[REGION], 5, (0, 255, 0), 3)
        return centered_coord

    # Where are we relative to our lane
    def where_lane_be(self):
        # Camera grab frame and normalize it
        self.grab_frame()
        self.normalize_img()

        # Filter out them colors
        self.ROI_blue, self.thres_blue = self.filter_smooth_thres(settings.BLUE_HSV_RANGE)
        self.ROI_yellow, self.thres_yellow = self.filter_smooth_thres(settings.YELLOW_HSV_RANGE)

        # Get contour meta data
        self.contour_metadata = self.get_contour_metadata()

        # Find center between lanes (we wanna try to be in there)
        self.center_coord = self.get_centered_coord()

        if self.debug:
            cv2.imshow('img', self.img)
            cv2.waitKey(0)

    # Use this to calculate fps
    def calculate_fps(self, frames_no=100):
        fps = FPS().start()

        # Don't wanna display window
        if self.debug:
            self.debug = not self.debug

        for i in range(0, frames_no):
            self.where_lane_be()
            fps.update()

        fps.stop()

        # Don't wanna display window
        if not self.debug:
            self.debug = not self.debug

        print('Time taken: {:.2f}'.format(fps.elapsed()))
        print('~ FPS : {:.2f}'.format(fps.fps()))

    # Destructor
    def __del__(self):
        self.vs.stop()
        cv2.destroyAllWindows()


