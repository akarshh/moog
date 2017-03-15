import serial, sys, datetime, time, smtplib
import numpy as np
from ISStreamer.Streamer import Streamer



# try:
# 	writer.writerow()
# except csv.Error
# 	pass

#f = open('testing.csv',"w")

streamer = Streamer(bucket_name="MoogTest", bucket_key="5LRM9UG8CASH",
                    access_key="NCbUQzFnRPMVoXDSjUL40Paxs0ICSV0Q")

arr = [0]*10000
# ser = serial.Serial('/dev/tty.usbmodem1411', 115200, 8, 'N', 1)
ser = serial.Serial('/dev/cu.usbmodem1421', 115200, 8, 'N', 1)

server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login("machinehealthgtmoog@gmail.com", "gtmoog2017")
msg = "Max Value higher than 500!"



while (ser.isOpen()):
	arrSum = 0
	start = time.time()
	
	for i in range(10000):
		try :
			arr[i] = int(ser.readline().rstrip('\r\n'))
		except ValueError:
			arr[i] = int(ser.readline().rstrip('\r\n'))

		# arr[i] = int(ser.readline().rstrip('\r\n'))
	avg = float(sum(arr))/10000
	maxVal = max(arr)
	finish = time.time()
	timeElapsed = finish-start
	stdDev = np.std(arr)

	if maxVal > 500:
		server.sendmail("machinehealthgtmoog@gmail.com", "machinehealthgtmoog@gmail.com", msg)
	# f.write('%.2f, \n' % avg)

	print('%.2f, %.2f, %i, %.2f' % (avg, timeElapsed, maxVal, stdDev))
	streamer.log("Average" , avg)
	streamer.log("Time" , timeElapsed)
	streamer.log("Maximum Value", maxVal)
	streamer.log("Standard Deviation", stdDev)

#f.close()
