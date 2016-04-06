class BlastGPIO(object):
    import os 
    # GPIO pin used to echo into /dev/servoblaster
    #
    # e.g. echo P1-GPIO_no=x > /dev/servoblaster
    def __init__(self, GPIO_no, min_threshold=1000, max_threshold=2000):
        self.GPIO_no = GPIO_no

        # Thresholding for outputs
        self.min_threshold = min_threshold
        self.max_threshold = max_threshold

    # Blast value into port
    def blast_value(self, val):
        os.system('echo P1-' + str(self.GPIO_no) + '=' + str(val) + 'us > /dev/servoblaster')

    def blast_neutral(self):
        n = str(int((self.max_threshold + self.min_threshold)/2))
        os.system('echo P1-' + str(self.GPIO_no) + '=' + n + 'us > /dev/servoblaster')



