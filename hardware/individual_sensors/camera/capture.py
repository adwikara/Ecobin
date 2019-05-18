import picamera
import time

def capture():
    with picamera.PiCamera() as camera:
        try:
            camera.resolution = (224,224)
            camera.ISO = 500
            camera.sharpness = 60
            camera.contrast = 60
            camera.brightness = 70
            #camera.start_preview()
            #time.sleep(3)
            camera.capture('trash.jpg')
            #camera.stop_preview()
        finally:
            camera.close()

#capture()