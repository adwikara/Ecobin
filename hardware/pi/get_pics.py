import picamera
import time
import RPi.GPIO as GPIO

def capture(i):
    with picamera.PiCamera() as camera:
        try:
            #.resolution = (224,224)
            camera.ISO = 500
            camera.sharpness = 60
            camera.contrast = 60
            camera.brightness = 70
            camera.start_preview()
            time.sleep(2)
            camera.capture('test' + str(i) + '.jpg')
            camera.stop_preview()
        finally:
            camera.close()
i = 1
#Setup GPIO Ports
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
inputLED = 13
GPIO.setup(inputLED, GPIO.OUT)
        
while(True):
    GPIO.output(inputLED, True)
    capture(i)
    i= i + 1
    time.sleep(5)
    GPIO.output(inputLED, False)