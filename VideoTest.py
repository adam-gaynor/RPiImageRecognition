from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2

#  Initialize and flip the camera
camera = PiCamera()
camera.resolution = (640, 480)
camera.vflip = True
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))

#  Give the camera time to warmup
time.sleep(.1)

#  Capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    # take the raw NumPy array representing the image, then initialize the timestamp
    # and occupied/unoccupied text
    image = frame.array

    #  Show the frame
    cv2.imshow("Frame", image)
    key = cv2.waitKey(1) & 0xFF

    #  Clear the stream to get ready for the next frame
    rawCapture.truncate(0)

    #  If the q key is pressed, break the loop
    if key == ord("q"):
        break
    



