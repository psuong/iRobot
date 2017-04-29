import socket

from .common import UDP_IP_PORT, Keys
import utility

if utility.does_module_exists('mraa'):
    import mraa
    import rover

    car = rover.RoverClient()
    car_move = True
else:
    car_move = False

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(UDP_IP_PORT)


def receive_loop():
    while True:
        data, addr = sock.recvfrom(1024)
        print("processing ", data)
        if car_move:
            if data == Keys.KEY_UP.value:
                car.forward()
            elif data == Keys.KEY_DOWN.value:
                car.backward()
            elif data == Keys.KEY_LEFT.value:
                car.forward_left()
            elif data == Keys.KEY_RIGHT.value:
                car.forward_right()
            elif data == Keys.KEY_SPACE.value:
                car.halt()
            else:
                print("got ", data)


if __name__ == '__main__':
    receive_loop()
