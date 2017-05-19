# iRobot
This repository for Professor Wei's Senior Design course, in which we build an autonomous rover which can detect lanes and stay on the lanes.

The project has strict dependencies on **OpenCV**.

## Branches
* `master` branch contains calibrated code for a 1080p camera
* `video-sample` branch contains code in which the algorithm attempts to predict the direction a car should move given a video.

## Setup
- Install Edison Drivers
- Use DC power outlet
- Connect to COM port, set the speed to 115200 as the speed in putty
- Update the WIFI parameters
    - For edits use `vim /etc/wpa_supplicant`
    - Update the configuration using `wpa_cli reconfigure`
- Change directories to the iRobot directory found in the SD Card
    - `cd /media/sdcard/iRobot`
- Run the backend server to receive commands
    - `mjpg_streamer -i "input_uvc.so -y -n -f 30 -r 320x240" -o "output_http.so -p 8080 -n -w /www/webcam" &`
    - This process MUST run as a bg process!

## Contributors
* Samuel Cohen
* Md Islam
* Porrith Suong