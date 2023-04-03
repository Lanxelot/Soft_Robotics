from ADCDACPi import ADCDACPi
import time


adcdac = ADCDACPi(1)
adcdac.set_adc_refvoltage(3.3)
while True:
	print(adcdac.read_adc_voltage(1,0))
	time.sleep(0.5)


	
	
	
