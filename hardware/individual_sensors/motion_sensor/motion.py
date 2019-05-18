import RPi.GPIO as GPIO
import time

def detect_motion(inputMotion):
    #Input port where RasPi receive signal from PIR
	i=GPIO.input(inputMotion)
	
	#When output from motion sensor is LOW
	if(i==0):
		#print("No Motion Detected")
		return False

    #When output from motion sensor is HIGH
	elif(i==1):
		#print("Motion Detected")
		return True
