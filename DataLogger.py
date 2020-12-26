#! /usr/bin/python3

#Modules
from sense_hat import SenseHat

sense = SenseHat()
sense.clear()

#Collect Data
pressure = sense.get_pressure()
temp = sense.get_temperature()
hum = sense.get_humidity()