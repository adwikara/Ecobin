#Import Libraries
import RPi.GPIO as GPIO
import time

def detect_capacity(inputTrigger, inputEcho):
    # set Trigger to HIGH
    GPIO.output(inputTrigger, True)

    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(inputTrigger, False)

    StartTime = time.time()
    StopTime = time.time()

    # save StartTime
    while GPIO.input(inputEcho) == 0:
        StartTime = time.time()

    # save time of arrival
    while GPIO.input(inputEcho) == 1:
        StopTime = time.time()

    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2

    #Return the distance to closest object in cm
    return distance