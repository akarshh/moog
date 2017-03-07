import serial, sys, datetime, time
import numpy as np
from ISStreamer.Streamer import Streamer
import smtplib;

streamer = Streamer(bucket_name="MoogTest", bucket_key="5LRM9UG8CASH",
                    access_key="NCbUQzFnRPMVoXDSjUL40Paxs0ICSV0Q")
server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login("machinehealthgtmoog@gmail.com", "gtmoog2017")
msg = "Max Val higher than 250"

arr = [0] * 10000
ser = serial.Serial('/dev/cu.usbmodem1411', 115200, 8, 'N', 1)
try:
    while ser.isOpen():
        arrSum = 0
        start = time.time()

        for i in range(10000):
            try:
                arr[i] = int(ser.readline().rstrip('\r\n'))
            except ValueError:
                arr[i] = int(ser.readline().rstrip('\r\n'))
        avg = float(sum(arr)) / 10000
        maxVal = max(arr)
        finish = time.time()
        stdDev = np.std(arr)
        if maxVal > 250:
            server.sendmail("machinehealthgtmoog@gmail.com", "machinehealthgtmoog@gmail.com", msg)
        print('%.2f, %.2f, %i, %.2f' % (avg, finish - start, maxVal, stdDev))
        streamer.log("Average", avg)
        streamer.log("Time", finish - start)
        streamer.log("Maximum", maxVal)
        streamer.log("Standard Deviation", stdDev)
except KeyboardInterrupt:
    pass

streamer.close()
server.close()
