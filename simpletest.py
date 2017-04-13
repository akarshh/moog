# Analog Data Collection from Machine Vibration Sensor 
import time
import numpy as np
import csv
import requests
import matplotlib.pyplot as plt
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

# Hardware SPI configuration:

def setupSystem():
	# Setup SPI for Data Collection
	SPI_PORT   = 0
	SPI_DEVICE = 0
	mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))
	return mcp



print('Reading MCP3008 values, press Ctrl-C to quit...')
# Currently Reading from Analog Channel #1 (8 channels from 0-7)
print('-' * 57)

def dataCollect(dataLength, mcp):
	start = time.time()
	global arr
	
	for i in range(dataLength):
		arr[i] = mcp.read_adc(1)
		
	avg = float(sum(arr))/dataLength
	maxVal = max(arr)
	stdDev = np.std(arr)
	finish = time.time()
	timeElapsed = finish - start
	return avg, maxVal, stdDev, timeElapsed

def printInfo(avg, maxVal, stdDev, timeElapsed):
	print("time elapsed: %.3f" % timeElapsed)
	print("average value: %0.3f" % avg)
	print("maximum value: %i" % maxVal)
	print("standard deviation: %0.3f" % stdDev)

def plotData(arr):
	y = [i for i in arr]
	x = [i for i in range(len(arr))]

	plt.plot(x,y)
	plt.show()

def saveData():
	now = time.strftime("%c")
	fileName = now + " Test Data.csv"
	myfile = open(fileName, 'wb')
	wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
	wr.writerow(arr)
	print("Data successfully saved to %s" % fileName)


def sendToGoogleScript(avg, maxVal, stdDev, timeElapsed):
	payload = {'average': avg, 'maxVal': maxVal, 'stdDev': stdDev, 'timeElapsed': timeElapsed}
	r = requests.post('https://script.google.com/macros/s/AKfycbzLbPSSnCXWE3XqGUrFFSr1H2TokeX0UfZRHWMLmymDzVb-1Ll9/exec', payload)

def main():
	mcp = setupSystem()
	avg, maxVal, stdDev, timeElapsed = dataCollect(len(arr), mcp)
	printInfo(avg, maxVal, stdDev, timeElapsed)
	saveData()
	sendToGoogleScript(avg, maxVal, stdDev, timeElapsed)
	plotData(arr)
	
if __name__ == "__main__":
	main()
	
