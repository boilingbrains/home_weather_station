#! /usr/bin/python3

#########
#Modules#
#########

import os
import sys
import time
import numpy as np
from sense_hat import SenseHat
from ISStreamer.Streamer import Streamer

###########
#Functions#
###########
#def match(element):
#    return bool(element[len(element)-3:len(element)] == 'png' )

def show_logo(images):
    for i in images:
        sense.load_image(i)
        time.sleep(1)
        
def check_conditions(param,selection,images2):
    #Check of required conditions 
    #Temperature: 18.3-26.7 Celsius
    #Pressure: 979-1027 millibars
    #Humidity: around 60%
    if selection == 'T':
        if param < 18.3 or param > 26.7:
            sense.load_image(images2[1])
        else:
            sense.load_image(images2[0])
    elif selection == 'P':
        if param < 979 or param > 1027:
            sense.load_image(images2[1])
        else:
            sense.load_image(images2[0])
    elif selection == 'H':
        if param < 60:
            sense.load_image(images2[1])
        else:
            sense.load_image(images2[0])
    
def display(sense, selection):
    # Draw the background (bg) selection box into another numpy array
    left, top, right, bottom = {
        'T': (0, 0, 4, 4),
        'P': (4, 0, 8, 4),
        'Q': (4, 4, 8, 8),
        'H': (0, 4, 4, 8),
        }[selection]
    bg = np.zeros((8, 8, 3), dtype=np.uint8)
    bg[top:bottom, left:right, :] = (255, 255, 255)
    # Construct final pixels from bg array with non-transparent elements of
    # the menu array
    sense.set_pixels([
        bg_pix if mask_pix else fg_pix
        for (bg_pix, mask_pix, fg_pix) in zip(
            (p for row in bg for p in row),
            (p for row in mask for p in row),
            (p for row in fg for p in row),
            )
        ])

def execute(sense,t,p,h, check_conditions, selection,images):
    if selection == 'T':
        sense.load_image(images[2])
        time.sleep(1)
        sense.show_message('T: %.1fC' % t, 0.05, Rd)
        check_conditions(t,selection,images2)
        time.sleep(1)
    elif selection == 'P':
        sense.load_image(images[1])
        time.sleep(1)
        sense.show_message('P: %.1fmbar' % p, 0.05, Gn)
        check_conditions(p,selection,images2)
        time.sleep(1)
    elif selection == 'H':
        sense.load_image(images[0])
        time.sleep(1)
        sense.show_message('H: %.1f%%' % h, 0.05, Bl)
        check_conditions(h,selection,images2)
        time.sleep(1)
    else:
        return True
    return False

def move(selection, direction):
    return {
        ('T', "right"): 'P',
        ('T', "down"):  'H',
        ('P', "left"):  'T',
        ('P', "down"):  'Q',
        ('Q', "up"):    'P',
        ('Q', "left"):  'H',
        ('H', "right"): 'Q',
        ('H', "up"):    'T',
        }.get((selection, direction), selection)
    
def get_cpu_temp():
  res = os.popen("vcgencmd measure_temp").readline()
  t = float(res.replace("temp=","").replace("'C\n",""))
  return(t)
def get_data(sense,logger):
    t1 = sense.get_temperature_from_humidity()
    t2 = sense.get_temperature_from_pressure()
    t_cpu = get_cpu_temp()
    # calculates the real temperature compesating CPU heating
    t = (t1+t2)/2
    t_corr = t - ((t_cpu-t)/1.5)
    t_corr = get_smooth(t_corr)
    logger.log("Temperature C", t_corr)
    p = sense.get_pressure()
    logger.log("Pressure mbar", p)
    h = sense.get_humidity()
    logger.log("Humidity %", h)
    return t_corr, p, h
## use moving average to smooth readings
def get_smooth(x):
  if not hasattr(get_smooth, "t"):
    get_smooth.t = [x,x,x]
  get_smooth.t[2] = get_smooth.t[1]
  get_smooth.t[1] = get_smooth.t[0]
  get_smooth.t[0] = x
  xs = (get_smooth.t[0]+get_smooth.t[1]+get_smooth.t[2])/3
  return(xs)

################
#initialization#
################
sense = SenseHat()
logger = Streamer(bucket_name="Sense Hat Sensor Data", access_key="ist_-QPaymsf-J1OLpzTH4MGCkT3X6Si_sgO")
sense.clear()

#Images
path = os.getcwd()+'/images/'
print(path)
images = [path+'logo/'+i for i in os.listdir(path+'logo/')]
images2 = [path+'conditions/'+i for i in os.listdir(path+'conditions/')]
#images = list(filter(match,images))

#Menu
Rd = (255, 0, 0)
Gn = (0, 255, 0)
Bl = (0, 0, 255)
Gy = (128, 128, 128)
__ = (0, 0, 0)

# Draw the foreground (fg) into a numpy array (8x8X3)
fg = np.array([
    [Rd, Rd, Rd, __, Gn, Gn, __, __],
    [__, Rd, __, __, Gn, __, Gn, __],
    [__, Rd, __, __, Gn, Gn, __, __],
    [__, Rd, __, __, Gn, __, __, __],
    [Bl, __, Bl, __, Gy, Gy, Gy, __],
    [Bl, Bl, Bl, __, Gy, __, Gy, __],
    [Bl, __, Bl, __, Gy, Gy, Gy, __],
    [Bl, __, Bl, __, __, Gy, Gy, __],
    ], dtype=np.uint8)

# Mask is a boolean array of which pixels are transparent
mask = np.all(fg == __, axis=2)
selection = 'T'
###########
# Process #
###########
try:
    sense.show_message("Hello")
    show_logo(images)
    sense.clear()
    sense.show_message("Menu")
    while True:
        display(sense,selection)
        t, p, h, = get_data(sense,logger)
        event = sense.stick.wait_for_event()
        if event.action == "pressed":
            if event.direction == "middle":
                if execute(sense,t,p,h,check_conditions, selection,images):
                    break
            else:
                selection = move(selection, event.direction)
    sense.clear()
except:
    #print("Something went wrong")
    sense.clear()

