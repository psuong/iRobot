import os

UDP_IP = os.environ.get('UDP_IP') or '127.0.0.1'
UDP_PORT = os.environ.get('UDP_PORT') or 5005

UDP_IP_PORT = (UDP_IP, UDP_PORT)