from BlastGPIO import *
import time

# Creates an instance of BlasterGPIO
servo = BlastGPIO(12)

# 1000us (turns left or right depending on configuration)
servo.blast_value(1000)

time.sleep(2)

# 2000us
servo.blast_value(2000)

time.sleep(2)

servo.blast_value(1500)
