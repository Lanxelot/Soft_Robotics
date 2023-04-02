import RPi.GPIO as GPIO
from time import sleep


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(12,GPIO.OUT)
pi = GPIO.PWM(12,1)
pi.start(50)
input('hhhh')
pi.stop()
GPIO.cleanup()
	



	
	
	
