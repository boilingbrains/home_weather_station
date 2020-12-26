#! /usr/bin/python3

#Modules
from sense_hat import SenseHat

sense = SenseHat()
sense.clear()

#Collect Data
pressure = sense.get_pressure()
temp = sense.get_temperature()
hum = sense.get_humidity()

#Check of required conditions 
#Temperature: 18.3-26.7 Celsius
#Pressure: 979-1027 millibars
#Humidity: around 60%


#Display
#Plot
