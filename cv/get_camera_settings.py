import picamera
import picamera.array
import numpy as np
import settings

with picamera.PiCamera() as camera:
    camera.resolution = (1280, 720)
    camera.awb_mode = 'off'
    # Start off with ridiculously low gains
    rg, bg = (0.5, 0.5)
    camera.awb_mode = settings.AWB_MODE
    camera.awb_gains = (rg, bg)
    camera.exposure_mode = settings.EXPOSURE_MODE
    camera.exposure_compensation = settings.EXPOSURE_COMPENSATION
    camera.saturation = settings.SATURATION
    camera.ISO = settings.ISO
    camera.brightness = settings.BRIGHTNESS
    camera.shutter_speed = settings.SHUTTER
    camera.contrast = settings.CONTRAST
    with picamera.array.PiRGBArray(camera, size=(128, 72)) as output:
        # Allow 30 attempts to fix AWB
        for i in range(30):
            # Capture a tiny resized image in RGB format, and extract the
            # average R, G, and B values
            camera.capture(output, format='rgb', resize=(128, 72), use_video_port=True)
            r, g, b = (np.mean(output.array[..., i]) for i in range(3))
            # Adjust R and B relative to G, but only if they're significantly
            # different (delta +/- 2)
            if abs(r - g) > 2:
                if r > g:
                    rg -= 0.1
                else:
                    rg += 0.1
            if abs(b - g) > 1:
                if b > g:
                    bg -= 0.1
                else:
                    bg += 0.1
            camera.awb_gains = (rg, bg)
            output.seek(0)
            output.truncate()

        print('---Camera output---')
        print('R: %5.2f, G:%5.2f, B:%5.2f' % (r, g, b))
        print('---Settings---')
        print('AWB mode\t|\t%s' % camera.awb_mode)
        print('AWB\t\t|\tR:%5.2f, B:%5.2f' % (rg, bg))
        print('Brightness\t|\t%5.2f' % camera.brightness)
        print('Contrast\t|\t%5.2f' % camera.contrast)
        print('ISO\t\t|\t%5.2f' % camera.ISO)
        print('Shutter Speed\t|\t%5.2f' % camera.shutter_speed)
        print('Saturation\t|\t%5.2f' % camera.saturation)
