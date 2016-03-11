import picamera
camera = picamera.PiCamera()
camera.vflip = True
camera.start_preview()

