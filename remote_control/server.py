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
        if car_move:
            print("got ", data)
            if data == Keys.KEY_UP:
                car.forward()
            elif data == Keys.KEY_DOWN:
                car.backward()
            elif data == Keys.KEY_LEFT:
                car.forward_left()
            elif data == Keys.KEY_RIGHT:
                car.forward_right()
            elif data == Keys.KEY_SPACE:
                car.halt()
            else:
                print("got ", data)


if __name__ == '__main__':
    receive_loop()
