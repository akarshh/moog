# Analog Data Collection from Machine Vibration Sensor 
import time
import sys
import os
import numpy as np
import csv
import requests
import matplotlib.pyplot as plt
from subprocess import call
import RPi.GPIO as gpio
from ISStreamer.Streamer import Streamer
from requests.exceptions import ConnectionError
# Import SPI library (for hardware SPI) and MCP3008 library.
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008


# Software SPI configuration:
#CLK  = 23
#MISO = 21
#MOSI = 19
#CS   = 24
#mcp = Adafruit_MCP3008.MCP3008(clk=CLK, cs=CS, miso=MISO, mosi=MOSI)

arr = [0]*100000

def shutdown(pin):
	call('halt', shell=False)

# Hardware SPI configuration:

def setupSystem():	
	# Setup SPI for Data Collection
	SPI_PORT   = 0
	SPI_DEVICE = 0
	mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))
	return mcp





# Collect Data and then process for specific information
def dataCollect(dataLength, mcp):
	print('Reading MCP3008 values, press Ctrl-C to quit...')
	gpio.output(19, gpio.HIGH)
	# Currently Reading from Analog Channel #1 (8 channels from 0-7)
	print('-' * 57)

	start = time.time()
	global arr
	
	for i in range(dataLength):
		arr[i] = mcp.read_adc(7)		
	avg = float(sum(arr))/dataLength
	maxVal = max(arr)
	stdDev = np.std(arr)
	finish = time.time()
	timeElapsed = finish - start
	gpio.output(19, gpio.LOW)
	return avg, maxVal, stdDev, timeElapsed

# Present information gathered to command line
def printInfo(avg, maxVal, stdDev, timeElapsed):
	print("time elapsed: %.3f" % timeElapsed)
	print("average value: %0.3f" % avg)
	print("maximum value: %i" % maxVal)
	print("standard deviation: %0.3f" % stdDev)

# Plot data for quick visualization
def plotData(arr):
	y = [i for i in arr]
	x = [i for i in range(len(arr))]

	plt.plot(x,y)
	plt.show()
	fileName = "Data_Plot.png"
	plt.savefig(fileName)
	plt.close('all')
	

# Save data to csv file with current date and time in file name
def saveData():
	now = time.strftime("%c")
	fileName = now + " Test Data.csv"
	myfile = open(fileName, 'wb')
	wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
	wr.writerow(arr)
	print("Data successfully saved to %s" % fileName)

# Package information for upload to google script
# Google script will further process data and write to google sheet
def sendToGoogleScript(avg, maxVal, stdDev, timeElapsed):
	payload = {'average': avg, 'maxVal': maxVal, 'stdDev': stdDev, 'timeElapsed': timeElapsed}
	# URL below is the specific google script that handles data collecting on the google sheet
	r = requests.post('https://script.google.com/macros/s/AKfycbzLbPSSnCXWE3XqGUrFFSr1H2TokeX0UfZRHWMLmymDzVb-1Ll9/exec', payload)
	return r

def sendToIS(streamer, avg, maxVal, stdDev, timeElapsed):
	streamer.log("Average" , avg)
	streamer.log("Standard Deviation" , maxVal)
	streamer.log("Maximum Value" , stdDev)
	streamer.log("Time Elapsed" , timeElapsed)

def main():
	gpio.setmode(gpio.BCM)
	gpio.setup(4, gpio.IN)
	gpio.setup(19, gpio.OUT)
	gpio.setup(16, gpio.OUT)
	gpio.add_event_detect(4, gpio.RISING, callback=shutdown, bouncetime=200)
	mcp = setupSystem()
	streamer = Streamer(bucket_name="MoogTest", bucket_key="5LRM9UG8CASH",access_key="NCbUQzFnRPMVoXDSjUL40Paxs0ICSV0Q")

	while int(time.strftime("%H")) <= 23:
		avg, maxVal, stdDev, timeElapsed = dataCollect(len(arr), mcp)
		if avg == 0 and maxVal == 0 and stdDev == 0:
			gpio.output(16, gpio.HIGH)
		else:
			gpio.output(16, gpio.LOW)
		printInfo(avg, maxVal, stdDev, timeElapsed)
		#saveData()
		try:
			r = sendToGoogleScript(avg, maxVal, stdDev, timeElapsed)
			sendToIS(streamer, avg, maxVal, stdDev, timeElapsed)
		except ConnectionError as e:
			r = "No response."
			print("Connection error. Check network settings.")
			gpio.output(16, gpio.HIGH)
		if r != "No response.":
			gpio.output(16, gpio.LOW)
	#~ try:
		#~ plotData(arr)
	#~ except KeyboardInterrupt:
		#~ print("Interrupted")
	#~ print("")

if __name__ == "__main__":
	try:
		main()
	except KeyboardInterrupt:
		print("Interrupted")
		gpio.output(16, gpio.LOW)
		gpio.output(19, gpio.LOW)
		try:
			sys.exit(0)
		except SystemExit:
			os._exit()
