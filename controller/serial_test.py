import serial
import time

ser = serial.Serial(
    port='/dev/ttyAMA0',
    baudrate=9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS
)

for i in range(0, 10):
    speed = 10*i
    ser.write('motor,'+str(speed))
    print('Speed: %s' % str(speed))
    time.sleep(1)
