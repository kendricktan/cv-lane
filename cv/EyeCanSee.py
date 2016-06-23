import time

import cv2
import numpy as np
import settings
from imutils.video import FPS
from imutils.video import WebcamVideoStream
from imutils.video.pivideostream import PiVideoStream


class EyeCanSee(object):
    def __init__(self, center=int(settings.CAMERA_WIDTH / 2), debug=False, is_usb_webcam=False):
        # Our video stream
        # If its not a usb webcam then get pi camera
        if not is_usb_webcam:
            self.vs = PiVideoStream(resolution=(settings.CAMERA_WIDTH, settings.CAMERA_HEIGHT))
            # Camera settings
            self.vs.camera.shutter_speed = settings.SHUTTER
            self.vs.camera.exposure_mode = settings.EXPOSURE_MODE
            self.vs.camera.exposure_compensation = settings.EXPOSURE_COMPENSATION
            self.vs.camera.awb_gains = settings.AWB_GAINS
            self.vs.camera.awb_mode = settings.AWB_MODE
            self.vs.camera.saturation = settings.SATURATION
            self.vs.camera.rotation = settings.ROTATION
            self.vs.camera.video_stabilization = settings.VIDEO_STABALIZATION
            self.vs.camera.ISO = settings.ISO
            self.vs.camera.brightness = settings.BRIGHTNESS
            self.vs.camera.contrast = settings.CONTRAST

        # Else get the usb camera
        else:
            self.vs = WebcamVideoStream(src=0)
            self.vs.stream.set(cv2.CAP_PROP_FRAME_WIDTH, settings.CAMERA_WIDTH)
            self.vs.stream.set(cv2.CAP_PROP_FRAME_HEIGHT, settings.CAMERA_HEIGHT)

        # Has camera started
        self.camera_started = False
        self.start_camera()  # Starts our camera

        # To calculate our error in positioning
        self.center = center

        # To determine if we actually detected lane or not
        self.detected_lane = False

        # debug mode on?
        self.debug = debug

    # Mouse event handler for get_hsv
    def on_mouse(self, event, x, y, flag, param):
        if event == cv2.EVENT_LBUTTONDBLCLK:
            # Circle to indicate hsv location, and update frame
            cv2.circle(self.img, (x, y), 3, (0, 0, 255))
            cv2.imshow('hsv_extractor', self.img)

            # Print values
            values = self.hsv_frame[y, x]
            print('H:', values[0], '\tS:', values[1], '\tV:', values[2])

    def get_hsv(self):
        cv2.namedWindow('hsv_extractor')
        while True:
            self.grab_frame()
            self.hsv_frame = cv2.cvtColor(self.img, cv2.COLOR_BGR2HSV)

            # Mouse handler
            cv2.setMouseCallback('hsv_extractor', self.on_mouse, 0)
            cv2.imshow('hsv_extractor', self.img)

            key = cv2.waitKey(0) & 0xFF
            if key == ord('q'):
                break
        self.stop_camera()
        cv2.destroyAllWindows()

    # Starts camera (needs to be called before run)
    def start_camera(self):
        self.camera_started = True
        self.vs.start()
        time.sleep(2.0)  # Wait for camera to cool

    def stop_camera(self):
        self.camera_started = False
        self.vs.stop()

    # Grabs frame from camera
    def grab_frame(self):
        # Starts camera if it hasn't been started
        if not self.camera_started:
            self.start_camera()
        self.img = self.vs.read()
        self.img_debug = self.img.copy()

    # Normalizes our image
    def normalize_img(self):
        # Crop img and convert to hsv
        self.img_roi = np.copy(self.img[settings.HEIGHT_PADDING:int(settings.HEIGHT_PADDING + 20), :])
        self.img_roi_hsv = cv2.cvtColor(self.img_roi, cv2.COLOR_BGR2HSV).copy()

        # Get our ROI's shape
        self.roi_height, self.roi_width, self.roi_channels = self.img_roi.shape

    # Smooth image and convert to bianry image (threshold)
    # Filter out colors that are not within the RANGE value
    def filter_smooth_thres(self, RANGE, color):
        for (lower, upper) in RANGE:
            lower = np.array(lower, dtype='uint8')
            upper = np.array(upper, dtype='uint8')

            mask = cv2.inRange(self.img_roi_hsv, lower, upper)

        blurred = cv2.medianBlur(mask, 5)

        # Morphological transformation
        kernel = np.ones((2, 2), np.uint8)
        smoothen = cv2.morphologyEx(blurred, cv2.MORPH_OPEN, kernel, iterations=5)

        if self.debug:
            cv2.imshow('mask ' + color, mask)
            cv2.imshow('blurred ' + color, blurred)
            cv2.imshow('smoothen ' + color, smoothen)

        return smoothen

    # Gets metadata from our contours
    def get_contour_metadata(self):

        # Metadata (x,y,w,h)for our ROI
        contour_metadata = {}
        for cur_img in [self.thres_yellow, self.thres_blue]:
            key = ''
            # Blue is left lane, Yellow is right lane
            if cur_img is self.thres_yellow:
                key = 'right'
            else:
                key = 'left'

            _, contours, hierarchy = cv2.findContours(cur_img.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

            cur_height, cur_width = cur_img.shape

            # Get index of largest contour
            try:
                areas = [cv2.contourArea(c) for c in contours]
                max_index = np.argmax(areas)
                cnt = contours[max_index]

                # Metadata of contour
                x, y, w, h = cv2.boundingRect(cnt)

                # Normalize it to the original picture
                x += int(settings.WIDTH_PADDING + w / 2)
                y += int(settings.HEIGHT_PADDING + h / 2)

                contour_metadata[key] = (x, y)

                self.detected_lane = True

                if self.debug:
                    cv2.circle(self.img_debug, (x, y), 5, (0, 0, 255), 2)

            # If it throws an error then it doesn't have a ROI
            # Means we're too far off to the left or right
            except:
                # Blue is left lane, Yellow is right lane

                x = int(settings.WIDTH_PADDING)
                y = int(cur_height / 2) + int(settings.HEIGHT_PADDING + cur_height / 2)

                if 'yellow' in key:
                    x += int(cur_width)

                contour_metadata[key] = (x, y)

                self.detected_lane = False

                if self.debug:
                    cv2.circle(self.img_debug, (x, y), 5, (0, 0, 255), 2)

        return contour_metadata

    # Gets the centered coord of the detected lines
    def get_centered_coord(self):
        centered_coord = None
        left_xy = self.contour_metadata['left']
        right_xy = self.contour_metadata['right']
        added_xy = (left_xy[0] + right_xy[0], left_xy[1] + right_xy[1])
        centered_coord = (int(added_xy[0] / 2), int(added_xy[1] / 2))

        if self.debug:
            cv2.circle(self.img_debug, centered_coord, 5, (0, 255, 0), 3)

        return centered_coord

    # Gets the error of the centered coordinates (x)
    def get_errors(self):
        return self.center_coord[0] - self.center

    # Where are we relative to our lane
    def where_lane_be(self):
        # Camera grab frame and normalize it
        self.grab_frame()
        self.normalize_img()

        # Filter out them colors
        self.thres_blue = self.filter_smooth_thres(settings.BLUE_HSV_RANGE, 'blue')
        self.thres_yellow = self.filter_smooth_thres(settings.YELLOW_HSV_RANGE, 'yellow')

        # Get contour meta data
        self.contour_metadata = self.get_contour_metadata()

        # Find center between lanes (we wanna try to be in there)
        self.center_coord = self.get_centered_coord()

        # Gets relative error
        self.relative_error = self.get_errors()

        if self.debug:
            cv2.imshow('img', self.img_debug)
            cv2.imshow('img_roi', self.img_roi)
            cv2.imshow('img_hsv', self.img_roi_hsv)
            cv2.imshow('thres_blue', self.thres_blue)
            cv2.imshow('thres_yellow', self.thres_yellow)
            key = cv2.waitKey(1) & 0xFF  # Change 1 to 0 to pause between frames

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

    # Use this to save images to a location
    def save_images(self, dirname='defisheye'):
        import os
        img_no = 1

        # Makes the directory
        if not os.path.exists('./' + dirname):
            os.mkdir(dirname)

        while True:
            self.grab_frame()

            if self.debug:
                cv2.imshow('frame', self.img)

            k = cv2.waitKey(1) & 0xFF

            if k == ord('s'):
                cv2.imwrite(os.path.join(dirname, 'fisheye_' + str(img_no) + '.jpg'), self.img)
                img_no += 1

            elif k == ord('q'):
                break

        cv2.destroyAllWindows()

    # Destructor
    def __del__(self):
        self.vs.stop()
        cv2.destroyAllWindows()
