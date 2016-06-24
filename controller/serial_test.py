import serial
import time

ser = serial.Serial('/dev/ttyUSB0', 9600)

for i in range(0, 10):
    speed = 10*i
    ser.write('motor,'+str(speed) + '\n')
    print('Speed: %s' % str(speed))
    time.sleep(0.25)

ser.write('motor,0\n')
