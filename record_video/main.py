# http://docs.opencv.org/3.1.0/dd/d43/tutorial_py_video_display.html#gsc.tab=0

# In this tutorial a video stream is read from the first video
# device on the computer and read back to the screen. It is
# also saved on the computer shortly afterwards

# import opencv
import cv2

# delcare a capture device as /dev/video0
capture = cv2.VideoCapture(0);

# declare a video-writing device to handle the output
# The h.264 video format is used for this (high compression, youtube)
fourcc = cv2.VideoWriter_fourcc(*'H264') 
# the * operator treats each byte as indexible element

# Output to capture.mp4
output = cv2.VideoWriter('video_capture.mkv', fourcc, 20.0, (640, 480))

# while the capture isn't interrupted.
while(capture.isOpened()):
  # capture frame by frame
  noErrors, frame = capture.read()

  if(noErrors):

    # Write each frame to the video file
    output.write(frame)

  # if quitting
  if(cv2.waitKey(1) & 0xFF == ord('q')):
    break;

# Release all stream listeners and quit
capture.release()
output.release()
cv2.destroyAllWindows()