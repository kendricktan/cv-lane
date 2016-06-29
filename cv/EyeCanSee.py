import time

import cv2
import numpy as np
import cvsettings
from imutils.video import FPS
from imutils.video import WebcamVideoStream
from imutils.video.pivideostream import PiVideoStream


class EyeCanSee(object):
    def __init__(self, center=int(cvsettings.CAMERA_WIDTH / 2), debug=False, is_usb_webcam=True, period_s=0.025):
        # Our video stream
        # If its not a usb webcam then get pi camera
        if not is_usb_webcam:
            self.vs = PiVideoStream(resolution=(cvsettings.CAMERA_WIDTH, cvsettings.CAMERA_HEIGHT))
            # Camera cvsettings
            self.vs.camera.shutter_speed = cvsettings.SHUTTER
            self.vs.camera.exposure_mode = cvsettings.EXPOSURE_MODE
            self.vs.camera.exposure_compensation = cvsettings.EXPOSURE_COMPENSATION
            self.vs.camera.awb_gains = cvsettings.AWB_GAINS
            self.vs.camera.awb_mode = cvsettings.AWB_MODE
            self.vs.camera.saturation = cvsettings.SATURATION
            self.vs.camera.rotation = cvsettings.ROTATION
            self.vs.camera.video_stabilization = cvsettings.VIDEO_STABALIZATION
            self.vs.camera.iso = cvsettings.ISO
            self.vs.camera.brightness = cvsettings.BRIGHTNESS
            self.vs.camera.contrast = cvsettings.CONTRAST

        # Else get the usb camera
        else:
            self.vs = WebcamVideoStream(src=0)
            self.vs.stream.set(cv2.CAP_PROP_FRAME_WIDTH, cvsettings.CAMERA_WIDTH)
            self.vs.stream.set(cv2.CAP_PROP_FRAME_HEIGHT, cvsettings.CAMERA_HEIGHT)

        # Has camera started
        self.camera_started = False
        self.start_camera()  # Starts our camera

        # To calculate our error in positioning
        self.center = center

        # To determine if we actually detected lane or not
        self.detected_lane = False

        # debug mode on? (to display processed images)
        self.debug = debug

        # Time interval between in update (in ms)
        # FPS = 1/period_s
        self.period_s = period_s

        # Starting time
        self.start_time = time.time()

    # Mouse event handler for get_hsv
    def on_mouse(self, event, x, y, flag, param):
        if event == cv2.EVENT_LBUTTONDBLCLK:
            # Circle to indicate hsv location, and update frame
            cv2.circle(self.img_debug, (x, y), 3, (0, 0, 255))
            cv2.imshow('hsv_extractor', self.img_debug)

            # Print values
            values = self.hsv_frame[y, x]
            print('H:', values[0], '\tS:', values[1], '\tV:', values[2])

    def get_hsv(self):
        cv2.namedWindow('hsv_extractor')
        while True:
            self.grab_frame()

            # Bottom ROI
            cv2.rectangle(self.img_debug, (0, cvsettings.HEIGHT_PADDING_BOTTOM-2), (cvsettings.CAMERA_WIDTH, cvsettings.HEIGHT_PADDING_BOTTOM + cvsettings.IMG_ROI_HEIGHT + 2), (0, 250, 0), 2)

            # Top ROI
            cv2.rectangle(self.img_debug, (0, cvsettings.HEIGHT_PADDING_TOP-2), (cvsettings.CAMERA_WIDTH, cvsettings.HEIGHT_PADDING_TOP + cvsettings.IMG_ROI_HEIGHT + 2), (0, 250, 0), 2)

            # Object
            cv2.rectangle(self.img_debug, (0, cvsettings.OBJECT_HEIGHT_PADDING), (cvsettings.CAMERA_WIDTH, cvsettings.HEIGHT_PADDING_TOP - cvsettings.OBJECT_HEIGHT_PADDING), (238, 130, 238), 2)

            self.hsv_frame = cv2.cvtColor(self.img, cv2.COLOR_BGR2HSV)

            # Mouse handler
            cv2.setMouseCallback('hsv_extractor', self.on_mouse, 0)
            cv2.imshow('hsv_extractor', self.img_debug)

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
        self.img_roi_bottom = np.copy(self.img[cvsettings.HEIGHT_PADDING_BOTTOM:int(cvsettings.HEIGHT_PADDING_BOTTOM + cvsettings.IMG_ROI_HEIGHT), :])
        self.img_roi_top = np.copy(self.img[cvsettings.HEIGHT_PADDING_TOP:int(cvsettings.HEIGHT_PADDING_TOP + cvsettings.IMG_ROI_HEIGHT), :])

        self.img_roi_bottom_hsv = cv2.cvtColor(self.img_roi_bottom, cv2.COLOR_BGR2HSV).copy()
        self.img_roi_top_hsv = cv2.cvtColor(self.img_roi_top, cv2.COLOR_BGR2HSV).copy()

        # Get our ROI's shape
        # Doesn't matter because both of them are the same shape
        self.roi_height, self.roi_width, self.roi_channels = self.img_roi_bottom.shape

    # Smooth image and convert to bianry image (threshold)
    # Filter out colors that are not within the RANGE value
    def filter_smooth_thres(self, RANGE, color):
        for (lower, upper) in RANGE:
            lower = np.array(lower, dtype='uint8')
            upper = np.array(upper, dtype='uint8')

            mask_bottom = cv2.inRange(self.img_roi_bottom_hsv, lower, upper)
            mask_top = cv2.inRange(self.img_roi_top_hsv, lower, upper)

        blurred_bottom = cv2.medianBlur(mask_bottom, 5)
        blurred_top = cv2.medianBlur(mask_top, 5)

        # Morphological transformation
        kernel = np.ones((2, 2), np.uint8)
        smoothen_bottom = blurred_bottom #cv2.morphologyEx(blurred, cv2.MORPH_OPEN, kernel, iterations=5)
        smoothen_top = blurred_top  # cv2.morphologyEx(blurred, cv2.MORPH_OPEN, kernel, iterations=5)

        """
        if self.debug:
            cv2.imshow('mask bottom ' + color, mask_bottom)
            cv2.imshow('blurred bottom' + color, blurred_bottom)

            cv2.imshow('mask top ' + color, mask_top)
            cv2.imshow('blurred top' + color, blurred_top)
        """

        return smoothen_bottom, smoothen_top

    # Gets metadata from our contours
    def get_contour_metadata(self):

        # Metadata (x,y,w,h)for our ROI
        contour_metadata = {}
        for cur_img in [self.thres_yellow_bottom, self.thres_yellow_top, self.thres_blue_bottom, self.thres_blue_top]:
            key = ''

            # Blue is left lane, Yellow is right lane
            if cur_img is self.thres_yellow_bottom:
                key = 'right_bottom'
            elif cur_img is self.thres_yellow_top:
                key = 'right_top'
            elif cur_img is self.thres_blue_bottom:
                key = 'left_bottom'
            elif cur_img is self.thres_blue_top:
                key = 'left_top'

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
                x += int(cvsettings.WIDTH_PADDING + w / 2)

                if 'top' in key:
                    y += int(cvsettings.HEIGHT_PADDING_TOP +h /2)
                else:
                    y += int(cvsettings.HEIGHT_PADDING_BOTTOM + h / 2)

                contour_metadata[key] = (x, y)

                self.detected_lane = True

            # If it throws an error then it doesn't have a ROI
            # Means we're too far off to the left or right
            except:

                # Blue is left lane, Yellow is right lane
                x = int(cvsettings.WIDTH_PADDING) - cvsettings.CAMERA_WIDTH

                if 'bottom' in key:
                    y = int(cur_height / 2) + int(cvsettings.HEIGHT_PADDING_BOTTOM + cur_height / 2)
                else:
                    y = int(cur_height / 2) + int(cvsettings.HEIGHT_PADDING_TOP + cur_height / 2)

                if 'right' in key:
                    x = int(cur_width)*2

                contour_metadata[key] = (x, y)

                self.detected_lane = False

        return contour_metadata

    # Gets the centered coord of the detected lines
    def get_centered_coord(self):
        bottom_centered_coord = None
        top_centered_coord = None

        left_xy_bottom = self.contour_metadata['left_bottom']
        right_xy_bottom = self.contour_metadata['right_bottom']

        left_xy_top = self.contour_metadata['left_top']
        right_xy_top = self.contour_metadata['right_top']

        bottom_xy = (left_xy_bottom[0] + right_xy_bottom[0], left_xy_bottom[1] + right_xy_bottom[1])
        bottom_centered_coord = (int(bottom_xy[0] / 2), int(bottom_xy[1] / 2))

        top_xy = (left_xy_top[0] + right_xy_top[0], left_xy_top[1] + right_xy_top[1])
        top_centered_coord = (int(top_xy[0] / 2), int(top_xy[1] / 2))

        # Left can't be greater than right and vice-versa
        if left_xy_top > right_xy_top:
            top_centered_coord = (0, top_centered_coord[1])
        elif right_xy_top < left_xy_top:
            top_centered_corrd = (cvsettings.CAMERA_WIDTH, top_centered_coord[1])

        if left_xy_bottom > right_xy_bottom:
            bottom_centered_coord = (0, bottom_centered_coord[1])
        elif right_xy_bottom < left_xy_bottom:
            bottom_centered_coord = (cvsettings.CAMERA_WIDTH, top_centered_coord[1])

        return bottom_centered_coord, top_centered_coord

    # Gets the error of the centered coordinates (x)
    # Also normlizes their values
    def get_errors(self):
        top_error = (float(self.center_coord_top[0]) - float(self.center))/float(cvsettings.CAMERA_WIDTH + cvsettings.WIDTH_PADDING)
        bottom_error = (float(self.center_coord_bottom[0]) - float(self.center))/float(cvsettings.CAMERA_WIDTH + cvsettings.WIDTH_PADDING)
        relative_error = (float(self.center_coord_top[0]) - float(self.center_coord_bottom[0]))/float(cvsettings.CAMERA_WIDTH + cvsettings.WIDTH_PADDING)

        return (top_error + relative_error + bottom_error)/3.0

    # Object avoidance
    def where_object_be(self):
        # We only want to detect objects in our path: center of top region and bottom region
        # So to save processing speed, we'll only threshold from center of top region to center of bottom region
        left_x = cvsettings.WIDTH_PADDING
        right_x = cvsettings.CAMERA_WIDTH

        # Image region with objects
        img_roi_object = self.img[cvsettings.OBJECT_HEIGHT_PADDING : int(cvsettings.HEIGHT_PADDING_TOP - cvsettings.OBJECT_HEIGHT_PADDING), left_x:right_x]
        img_roi_object_hsv = cv2.cvtColor(img_roi_object, cv2.COLOR_BGR2HSV).copy()

        # Filtering color and blurring
        for (lower, upper) in cvsettings.OBJECT_HSV_RANGE:
            lower = np.array(lower, dtype='uint8')
            upper = np.array(upper, dtype='uint8')

            mask_object = cv2.inRange(img_roi_object_hsv, lower, upper)

        blurred_object = cv2.medianBlur(mask_object, 25)

        # Finding position of object (if its there)
        _, contours, hierarchy = cv2.findContours(blurred_object.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        left_x = self.contour_metadata['left_top'][0]
        right_x = self.contour_metadata['right_top'][0]

        for c in contours:
            areas = cv2.contourArea(c)

            # Object needs to be larger than a certain area
            if areas > cvsettings.OBJECT_AREA:
                x, y, w, h = cv2.boundingRect(c)

                y += int(cvsettings.OBJECT_HEIGHT_PADDING + h / 2)

                # Confusing part - this finds the object and makes it think that
                # it is also a line to avoid bumping into it
                # It +w and -w to find which line its closest to and then set
                # the opposite as to be the new left/right lane
                # e.g. line is closest to left lane (x-w), so left lane new x is
                # (x+w)

                distance_to_left = abs(x - left_x)
                distance_to_right = abs(x+w - right_x)

                # Make object's left most area the middle of right lane
                if distance_to_left > distance_to_right:
                    self.contour_metadata['right_top'] = (x, self.contour_metadata['right_top'][1])

                # Make object's right most area the middle of left lane
                elif distance_to_right > distance_to_right:
                    self.contour_metadata['left_top'] = (x+w, self.contour_metadata['left_top'][1])

                if self.debug:
                    cv2.circle(self.img_debug, (x+(w/2), y+(h/2)), 5, (240, 32, 160), 2)

        if self.debug:
            cv2.imshow('Blurred object', blurred_object)


    # Where are we relative to our lane
    def where_lane_be(self):
        # Running once every period_ms
        while float(time.time() - self.start_time) < self.period_s:
            pass

        # Update time instance
        self.start_time = time.time()

        # Camera grab frame and normalize it
        self.grab_frame()
        self.normalize_img()

        # Filter out them colors
        self.thres_blue_bottom, self.thres_blue_top = self.filter_smooth_thres(cvsettings.BLUE_HSV_RANGE, 'blue')
        self.thres_yellow_bottom, self.thres_yellow_top = self.filter_smooth_thres(cvsettings.YELLOW_HSV_RANGE, 'yellow')

        # Get contour meta data
        self.contour_metadata = self.get_contour_metadata()

        # Finds objects and (and corrects lane position)
        # this overwrite contour_metadata
        #self.where_object_be()

        # Find the center of the lanes (bottom and top) [we wanna be in between]
        self.center_coord_bottom, self.center_coord_top = self.get_centered_coord()

        # Gets relative error between top center and bottom center
        self.relative_error = self.get_errors()

        if self.debug:
            # Drawing locations
            blue_top_xy = self.contour_metadata['left_top']
            blue_bottom_xy = self.contour_metadata['left_bottom']
            yellow_top_xy = self.contour_metadata['right_top']
            yellow_bottom_xy = self.contour_metadata['right_bottom']

            # Circles to indicate lanes
            cv2.circle(self.img_debug, blue_top_xy, 5, (255, 0, 0), 2)
            cv2.circle(self.img_debug, blue_bottom_xy, 5, (255, 0, 0), 2)
            cv2.circle(self.img_debug, yellow_top_xy, 5, (0, 255, 255), 2)
            cv2.circle(self.img_debug, yellow_bottom_xy, 5, (0, 255, 255), 2)
            cv2.circle(self.img_debug, self.center_coord_bottom, 5, (0, 255, 0), 3)
            cv2.circle(self.img_debug, self.center_coord_top, 5, (0, 255, 0), 3)

            # ROI for object detection
            cv2.rectangle(self.img_debug, (0, cvsettings.OBJECT_HEIGHT_PADDING), (cvsettings.CAMERA_WIDTH, cvsettings.HEIGHT_PADDING_TOP - cvsettings.OBJECT_HEIGHT_PADDING), (238, 130, 238), 2)

            # Displaying image
            cv2.imshow('img', self.img_debug)
            #cv2.imshow('img_roi top', self.img_roi_top)
            #cv2.imshow('img_roi bottom', self.img_roi_bottom)
            #cv2.imshow('img_hsv', self.img_roi_hsv)
            cv2.imshow('thres_blue_bottom', self.thres_blue_bottom)
            cv2.imshow('thres_blue_top', self.thres_blue_top)
            cv2.imshow('thres_yellow_bottom', self.thres_yellow_bottom)
            cv2.imshow('thres_yellow_top', self.thres_yellow_top)
            key = cv2.waitKey(0) & 0xFF  # Change 1 to 0 to pause between frames

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
    def save_images(self, dirname='dump'):
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
                cv2.imwrite(os.path.join(dirname, 'dump_' + str(img_no) + '.jpg'), self.img)
                img_no += 1

            elif k == ord('q'):
                break

        cv2.destroyAllWindows()
    # Destructor
    def __del__(self):
        self.vs.stop()
        cv2.destroyAllWindows()
