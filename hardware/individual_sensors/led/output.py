import RPi.GPIO as GPIO

def outputSignal(trashSignal, recySignal, signal = False):
    redLED = trashSignal
    greenLED = recySignal

    if (signal == True):
        GPIO.output(greenLED, True)
    else:
        GPIO.output(redLED, True)



