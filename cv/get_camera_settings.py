import io
import time
import picamera
import picamera.array
import cv2
import numpy as np
import cvsettings

# Create the in-memory stream
stream = io.BytesIO()

with picamera.PiCamera() as camera:
    camera.resolution = (cvsettings.CAMERA_WIDTH, cvsettings.CAMERA_HEIGHT)
    camera.awb_mode = 'auto'
    camera.exposure_mode = 'auto'

    time.sleep(2)

    camera.start_preview()
    time.sleep(2)
    camera.capture(stream, format='jpeg')

    print('---Settings---')
    print('AWB mode\t|\t%s' % camera.awb_mode)
    print('AWB\t\t|\t%s' % (camera.awb_gains,))
    print('Brightness\t|\t%5.2f' % camera.brightness)
    print('Contrast\t|\t%5.2f' % camera.contrast)
    print('ISO\t\t|\t%5.2f' % camera.ISO)
    print('Shutter Speed\t|\t%5.2f' % camera.shutter_speed)
    print('Saturation\t|\t%5.2f' % camera.saturation)
    print('Exposure Mode\t|\t%s' % camera.exposure_mode)
    print('Exposure Compensation\t|\t%5.2f' % camera.exposure_compensation)

# Construct a numpy array from the stream
data = np.fromstring(stream.getvalue(), dtype=np.uint8)

# "Decode" the image from the array, preserving colour
image = cv2.imdecode(data, 1)

cv2.imshow('image', image)
cv2.waitKey(0)
