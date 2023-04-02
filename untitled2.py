#####################################################################################
# Import the required Python Libraries
#####################################################################################

import RPi.GPIO as GPIO
import time

#####################################################################################
# Define the Variables Needed and the GPIO initialisation
#####################################################################################


global pwmobj                    # declare the pmwobj as a global variable
RPI_Pin = 12                     # define the RPI GPIO Pin we will use with PWM (PWM)
RPI_DutyCycle = 50               # define the Duty Cycle in percentage  (50%)
RPI_Freq = 1                   # define the frequency in Hz (500Hz)
RPI_LEDTime = 60                 # the time you want the LED to stay lit for (secs)
GPIO.setmode(GPIO.BOARD)              # set actual GPIO BCM Numbers
GPIO.setup(RPI_Pin, GPIO.OUT)         # set RPI_PIN as OUTPUT mode
GPIO.output(RPI_Pin, GPIO.LOW)        # set RPI_PIN LOW to at the start
pwmobj = GPIO.PWM(RPI_Pin, RPI_Freq)  # Initialise instance and set Frequency
pwmobj.start(0)                       # set initial Duty cycle to 0 & turn on PWM

#####################################################################################
# Define our main task
#####################################################################################

def light():
    pwmobj.ChangeDutyCycle(RPI_DutyCycle)               # Set PWM Duty Cycle to 50%
    time.sleep(RPI_LEDTime)                             # Keep Led lit for 60 secs

#####################################################################################
# Define our DESTROY Function
#####################################################################################

def destroy():
    pwmobj.stop()                                               # stop PWM

#####################################################################################
# Finally the code for the MAIN program
#####################################################################################

if __name__ == '__main__':                                      # Program entry point
    print ('LED Turned on with Duty Cycle of ', RPI_DutyCycle)  # Print duty cycle
    try:
        light()                                                 # call light function
    except KeyboardInterrupt:                                   # Watches for Ctrl-C
        destroy()                                               # call destroy funct
    finally:
        destroy()                                               # call destroy funct



import tkinter as tk
import RPi.GPIO as GPIO
import threading

# Replace this with the GPIO pin number you are using for PWM
PWM_PIN = 18

# Replace these with the desired PWM frequency and duty cycle
PWM_FREQ = 100
PWM_DUTY_CYCLE = 50

# Set up the GPIO pin for PWM
GPIO.setmode(GPIO.BCM)
GPIO.setup(PWM_PIN, GPIO.OUT)
pwm = GPIO.PWM(PWM_PIN, PWM_FREQ)
pwm.start(PWM_DUTY_CYCLE)

# Create a Tkinter window with a button widget
root = tk.Tk()

def on_button_press():
    # This function will be called when the button is pressed
    # Start a new thread to control the PWM duty cycle
    threading.Thread(target=update_pwm_duty_cycle).start()

def update_pwm_duty_cycle():
    # This function will run in a separate thread
    # Check the state of the button widget and adjust the PWM duty cycle accordingly
    while button_state.get():
        duty_cycle = PWM_DUTY_CYCLE if button_state.get() else 0
        pwm.ChangeDutyCycle(duty_cycle)

# Create a button widget and associate it with a Tkinter variable
button_state = tk.BooleanVar()
button = tk.Checkbutton(root, text="Generate PWM", variable=

	



