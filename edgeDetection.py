import picamera
import numpy as np
import cv2
camera = picamera.PiCamera()
camera.vflip = True
camera.start_preview()

