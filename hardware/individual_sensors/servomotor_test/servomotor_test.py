import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BOARD)

# Set Pins
servo_pin=18
GPIO.setup(servo_pin,GPIO.OUT)
pwm=GPIO.PWM(servo_pin,50) # (Pin Number, Hz)
pwm.start(7.5)

def sort(x):
    if x=='Recyclable':
        pwm.ChangeDutyCycle(0)
        sleep(0.5)
        pwm.ChangeDutyCycle(7.5)
        pwm.stop()
    elif x=='Trash':
        pwm.ChangeDutyCycle(12.5)
        sleep(0.5)
        pwm.ChangeDutyCycle(0)
        pwm.stop()
        
sort('Trash')
sleep(2)
sort('Recyclable')
pwm.stop()
exit()