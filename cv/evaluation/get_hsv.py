import cv2
import numpy as np

WIDTH = 640
HEIGHT = 480

x_co = 0
y_co = 0

def on_mouse(event,x,y,flag,param):
    global x_co, y_co
    x_co = x
    y_co = y

# Get vidoe feed
cap = cv2.VideoCapture(0)

# Set camera parameters
#cap.set(cv2.CAP_PROP_GAIN, 0.3)
#cap.set(cv2.CAP_PROP_BRIGHTNESS, 0.2)

# Get camera parameters
#print('Capture mode: '+ str(cap.get(cv2.CAP_PROP_MODE)))
#print('Capture brightness: '+ str(cap.get(cv2.CAP_PROP_BRIGHTNESS)))

cv2.namedWindow('camera')

while True:
    ret, frame = cap.read()
    #frame = cv2.imread('../../img/highway.jpg')

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    cv2.setMouseCallback("camera", on_mouse, 0)

    try:
        values = hsv[y_co, x_co]
        print('H:', values[0], '\tS:', values[1], '\tV:', values[2])
    except:
        pass

    cv2.imshow('camera', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
