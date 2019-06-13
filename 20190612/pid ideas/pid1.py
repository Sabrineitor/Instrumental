# from hgrecco

##########
# Caso 3
##########

def PIDFun(feedback_value, setpoint, kp, ki, kd, last_error, i_term):
    error = setpoint - feedback_value

    delta_error = error - last_error

    p_term = kp * error
    i_term += error
    d_term = delta_error

    last_error = delta_error

    return p_term + (ki * i_term) + (kd * d_term), last_error, i_term


while True:

    signal = read()

    actuator, last_error, i_term = PIDFun(signal, 42, 3, 2, 1, last_error, i_term)

    write(actuator)




##########
# Caso 3b
##########

def create_PIDfun(setpoint, kp, ki, kd):

    last_error = 0
    i_term = 0

    def _internal(feedback_value):

        nonlocal last_error
        nonlocal i_term

        error = setpoint - feedback_value

        delta_error = error - last_error

        p_term = kp * error
        i_term += error
        d_term = delta_error

        last_error = delta_error

        return p_term + (ki * i_term) + (kd * d_term), last_error, i_term

    return _internal


lazo = create_PIDfun(42, 3, 2, 1)

while True:

    signal = read()

    actuator = lazo(signal)

    write(actuator)


##########
# Caso 4
##########


class PIDController:

    def __init__(self, setpoint, kp=1.0, ki=0.0, kd=0.0):

        self.setpoint = setpoint
        self.kp = kp
        self.ki = ki
        self.kd = kd

        self.last_error = 0
        self.p_term = 0
        self.i_term = 0
        self.d_term = 0

    def calculate(self, feedback_value):
        error = self.setpoint - feedback_value

        delta_error = error - self.last_error

        self.p_term = self.kp * error
        self.i_term += error
        self.d_term = delta_error

        self.last_error = error

        return self.p_term + (self.ki * self.i_term) + (self.kd * self.d_term)



lazo = PIDController(42, 3, 2, 1)

while True:

    signal = read()

    actuator = lazo.calculate(signal)

    write(actuator)


##########
# Caso 5
##########


def PIDgen(setpoint, kp, ki, kd):

    last_error = 0
    i_term = 0

    output = 0

    while True:

        feedback_value = yield output

        error = setpoint - feedback_value

        delta_error = error - last_error

        p_term = kp * error
        i_term += error
        d_term = delta_error

        last_error = delta_error

        output = p_term + (ki * i_term) + (kd * d_term), last_error, i_term



lazo = PIDGen(42, 3, 2, 1)

lazo.send(None)

while True:

    signal = read()

    actuator = lazo.send(signal)

write(actuator)
