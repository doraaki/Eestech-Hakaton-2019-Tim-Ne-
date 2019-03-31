#!/usr/bin/env python2.7

from sys import stdout
from sys import exit
from time import sleep
from Adafruit_BMP085 import BMP085

bmp = BMP085(0x77)

while True:

        try:

                temp = bmp.readTemperature()
		pressure = bmp.readPressure()
		print "Temperature: %.2f C" % temp
		print "Pressure:    %.2f hPa" % (pressure / 100.0)
        except KeyboardInterrupt:

                break

exit()
