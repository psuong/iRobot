# http://stackoverflow.com/questions/32300000/galileo-and-ultrasonic-error-when-distance-less-than-4cm
import mraa
import time


def trig_echo(trig_port=3, echo_port=4):
    trig = mraa.Gpio(trig_port)
    echo = mraa.Gpio(echo_port)

    trig.dir(mraa.DIR_OUT)
    echo.dir(mraa.DIR_IN)

    return trig, echo

def distance(measure='cm', trig=trig, echo=echo):
    trig.write(0)
    time.sleep(0.1)

    trig.write(1)
    time.sleep(0.00001)
    trig.write(0)

    while echo.read() == 0:
            nosig = time.time()
    sig = None
    while echo.read() == 1:
            sig = time.time()

    if sig is None:
        return -1
    # et = Elapsed Time
    et = sig - nosig

    if measure == 'cm':
            distance =  et * 17150
    elif measure == 'in':
            distance = et / 0.000148
    else:
            print('improper choice of measurement!!')
            distance = None

    return distance if distance < 80 else -1

if __name__ == '__main__':
    while True:
        print(distance('cm'))
        time.sleep(1)
