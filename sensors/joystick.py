from mraa import Aio

from rover import RoverClient, Move

X_PIN = 0
Y_PIN = 1

vr_x = Aio(X_PIN)
vr_y = Aio(Y_PIN)


if __name__ == '__main__':
    rover = RoverClient()
    while True:
        x, y = vr_x.read(), vr_y.read()
        if y == 0 and 500 < x < 600:
            rover.send(Move.FORWARD)
        elif y > 1000 and 500 < x < 600:
            rover.send(Move.BACKWARD)
        elif x == 0 and 500 < y < 600:
            rover.send(Move.LEFT)
        elif x > 1000 and 300 < y < 600:
            rover.send(Move.RIGHT)
        else:
            pass
