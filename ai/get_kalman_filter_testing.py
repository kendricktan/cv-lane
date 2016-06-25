import random

from KalmanFilter import *
from aisettings import *

kalman_filter = KalmanFilter(VAR, EST_VAR)

for i in range(5, 50):
    num = random.randint(-10, 10)

    kalman_filter.input_latest_noisy_measurement(num)
    filtered_value = kalman_filter.get_latest_estimated_measurement()

    print("Estimated:\t%s\t|\tActual:\t%s" % (num, filtered_value))
