from capture import capture
from motion import detect_motion
from ultrasonic import detect_capacity
from sort_motor import sort
import RPi.GPIO as GPIO
import time
from PIL import Image
import numpy as np
from raspirequests import getdata, putdata
#from pymongo import MongoClient
import base64

#Ecobin Program
if __name__ == '__main__':
    try:
        #Setup GPIO Board
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        
        #Setup Pins
        inputMotion = 7
        inputLid = 15
        inputLED = 13
        inputTrigger = 18
        inputEcho = 24

        #Setup input/output ports
        GPIO.setup(inputLid, GPIO.OUT) #Automatic Lid
        GPIO.setup(inputLED, GPIO.OUT) #LED Strip
        GPIO.setup(inputMotion, GPIO.IN) #PIR Motion Sensor
        GPIO.setup(inputTrigger, GPIO.OUT) #Ultrasonic output
        GPIO.setup(inputEcho, GPIO.IN) #Ultrasonic input
        

        #Initialize Ports
        GPIO.output(inputLid, False)
        GPIO.output(inputLED, False)

        #Ecobin Process Starts
        while(True):
            #Capacity Detection
            fullCapacity = 63 #25 inches ~ 63.5 cm
            ultrasonicValue = detect_capacity(inputTrigger, inputEcho)

            #Get distance from closest trash pile
            distance = fullCapacity - ultrasonicValue

            #Compute the capacity
            capacity = (((fullCapacity - distance)/fullCapacity) * 100)

            #Put the capacity value in the API
            putdata("capacity", capacity)

            #Object Detection
            motion = detect_motion(inputMotion)
            if (motion == True):
                print("Motion detected")

                #Turn on the LED strip
                GPIO.output(inputLED, True)

                #Configure the lid
                GPIO.output(inputLid, True) #Lid opens
                time.sleep(2)
                GPIO.output(inputLid, False) #Lid closes
                
                #Take picture
                capture()
                
                #Turn of LED strip
                GPIO.output(inputLED, False)

                #Get Image From Directory
                im = open("trash.jpg", "rb")
                #print(image_array)
                
                #Converting the image into a numpy array
                np_im = np.array(im)
                imagestring = base64.b64encode(im.read())
                
                #Put encoded picture in API
                putdata("string", str(imagestring))

                #Wait for backend to process
                time.sleep(2)

                #Retrieve type of object from API
                type = getdata()
                #print(type)

                #Sorting Motor
                if (type == 'trash'):
                    sort(160000)
                    #time.sleep(1)
                    #sort(-140000)
                elif (type == 'recyclable'):
                    sort(-160000)
                    #time.sleep(1)
                    #sort(140000)
                else:
                    pass
                
                #The PIR sensor outputs signals for roughly 5 seconds, so we set sleep = 5s to avoid duplicates
                time.sleep(6)

            else:
                print ("No Motion Detected")
                time.sleep(1)

    # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Ecobin Shut Down")
        GPIO.cleanup()