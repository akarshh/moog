import serial, sys, datetime, time
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
ser = serial.Serial('/dev/cu.usbmodem1411', 230400, 8, 'N', 1)



# with open(sys.argv[3], "w") as f:
#   with serial.Serial(port=sys.argv[1], baudrate=sys.argv[2]) as ser:
#     if ser.isOpen():
#       ser.readline()
#     while ser.isOpen():
#       f.write('{}, {}'.format(datetime.datetime.now().strftime('%c'), ser.readline()))



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
	stdDev = np.std(arr)
	# f.write('%.2f, \n' % avg)

	print('%.2f, %.2f, %i, %.2f' % (avg, finish-start, maxVal, stdDev))
	streamer.log("My Numbers" , avg)

#f.close()
