# Stream Video with OpenCV from an Android running IP Webcam (https://play.google.com/store/apps/details?id=com.pas.webcam)
# Code Adopted from http://stackoverflow.com/questions/21702477/how-to-parse-mjpeg-http-stream-from-ip-camera

import cv2
from urllib.request import urlopen
import numpy as np
import sys

host = "172.16.12.47:8080"
if len(sys.argv)>1:
    host = sys.argv[1]

hoststr = 'http://' + host + '/video'
print('Streaming ' + hoststr)

stream= urlopen(hoststr)

byte=b''
while True:
    print('reading byte')
    byte+=stream.read(1024)
    a = byte.find(b'\xff\xd8')
    b = byte.find(b'\xff\xd9')
    if a!=-1 and b!=-1:
        jpg = byte[a:b+2]
        byte= byte[b+2:]
        image = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), 0)
        cv2.imshow(hoststr, image)
        if cv2.waitKey(1) ==27:
            exit(0)


