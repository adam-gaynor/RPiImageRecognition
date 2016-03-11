from picamera.array import PiRGBArray
from picamera import PiCamera
import argparse
import imutils
import time
import cv2

#  DEFINE CONSTANT VARIABLES
camera_warmup_time = 2.5
framerate = 32
min_area = 5000
#  Initialize and flip the camera
camera = PiCamera()
camera.resolution = (640, 480)
camera.vflip = True
camera.framerate = framerate
rawCapture = PiRGBArray(camera, size=(640, 480))

#  Give the camera time to warmup
time.sleep(camera_warmup_time)

#  contruct argument parser and parse arguments
ap = argparse.ArgumentParser()
#  ap.add_argument("-a", "--min-area", type=int, default=500, help="minimum area size") #  Sets minimum size for motion to be considered
args = vars(ap.parse_args())

#  Delay until camera is ready, then store initialize first frame and motion counter
time.sleep(.3)
firstFrame = None
motionCounter = 0

#  Begin capturing frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    #  Take the raw NumPy array representing the image and Movement/No Movement text
    image = frame.array
    text = "No Movement Detected"

    #  Resize the frame, convert it to grayscale, and blur it for easier processing
    image = imutils.resize(image, width = 500)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21,21), 0)

    #  Save the background frame for movement comparison later
    if firstFrame is None:
        firstFrame = gray.copy().astype("float")
        rawCapture.truncate(0)
        continue

    #  Accumulate the weighted average between the current frame and previous frames, then compute
    #  the difference between the current frame and the weighted average
    cv2.accumulateWeighted(gray, firstFrame, .5)
    frameDelta = cv2.absdiff(gray, cv2.convertScaleAbs(firstFrame))

    #  Fill holes in threshold image and find contours on threshold image
    thresh = cv2.threshold(frameDelta, 5, 255, cv2.THRESH_BINARY)[1]
    thresh = cv2.dilate(thresh, None, iterations=2)
    (_, cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    #  Loop over the contours

    for c in cnts:
        if cv2.contourArea(c) < min_area:
            continue
        #  Find bounding box for the contour, draw it on the frame, and update text to show movement
        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
        text = "Movement Detected"
        cv2.putText(image, text, (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                (0, 0, 255), 2)

    #  Show the frame
    cv2.imshow("IMAGE DETECTION PROJECT", image)
    key = cv2.waitKey(1) & 0xFF

    #  If the q key is pressed, break the loop
    if key == ord("q"):
        break
    
    #  Clear the stream to get ready for the next frame
    rawCapture.truncate(0)
    



