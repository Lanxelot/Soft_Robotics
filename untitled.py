import RPi.GPIO as GPIO
import scipy
import numpy as np
from scipy import signal
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
channel = 8
GPIO.setup(channel,GPIO.OUT)


def turn_on():
	tim = np.linspace(0,10,100,endpoint = False)
	y = signal.square(2*np.pi*10*tim,duty = 0.5)
	y[y==-1.0] = False
	y[y==1.0] = True
	for x in y:
		GPIO.output(channel,int(x))
		
	



if __name__ == "__main__":
   turn_on()
