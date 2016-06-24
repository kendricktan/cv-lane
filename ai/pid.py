class PID:
    def __init__(self, p=.5, i=0.0, d=0.0, derivator=0, integrator=0, integrator_max=50, integrator_min=-50, min_threshold=-10, max_threshold=10):
        self.kp = p
        self.ki = i
        self.kd = d

        self.derivator = derivator
        self.integrator = integrator
        self.integrator_max = integrator_max
        self.integrator_min = integrator_min

        self.min_threshold = min_threshold
        self.max_threshold = max_threshold

        self.error = 0

    def update(self, error):
        self.error = error

        self.p_val = self.kp * self.error
        self.d_val = self.kd * (self.error - self.derivator)
        self.derivator = self.error

        self.integrator = self.integrator + self.error

        if self.integrator > self.integrator_max:
            self.integrator = self.integrator_max
        elif self.integrator < self.integrator_min:
            self.integrator = self.integrator_min

        self.i_val = self.integrator * self.ki

        pid = self.p_val + self.i_val + self.d_val

        if pid < self.min_threshold:
            pid = self.min_threshold
        elif pid > self.max_threshold:
            pid = self.max_threshold

        return pid

    def setPoint(self, set_point):
        self.set_point = set_point
        self.integrator = 0
        self.derivator = 0
