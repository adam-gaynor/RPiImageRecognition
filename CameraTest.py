from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2

#  Initialize and flip the camera
camera = PiCamera()
camera.vflip = True
rawCapture = PiRGBArray(camera)

#  Give the camera time to warmup
time.sleep(.1)

#  Snap a picture with the camera
camera.capture(rawCapture, format="bgr")
image = rawCapture.array

#display the image on a screen and wait for keypress
cv2.imshow("Image", image)
cv2.waitKey(0)


