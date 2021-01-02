#! /usr/bin/python3

#########
#Modules#
#########
from sense_hat import SenseHat
import numpy as np
import time
import os

###########
#Functions#
###########
def match(element):
    return bool(element[len(element)-3:len(element)] == 'png' )

def show_logo(images):
    print(images)
    for i in images:
        print(i)
        sense.load_image(path+i)
        time.sleep(1)

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

def execute(sense, selection,images):
    if selection == 'T':
        sense.load_image(images[2])
        time.sleep(1)
        sense.show_message('T: %.1fC' % sense.temp, 0.05, Rd)
    elif selection == 'P':
        sense.load_image(images[1])
        time.sleep(1)
        sense.show_message('P: %.1fmbar' % sense.pressure, 0.05, Gn)
    elif selection == 'H':
        sense.load_image(images[0])
        time.sleep(1)
        sense.show_message('H: %.1f%%' % sense.humidity, 0.05, Bl)
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


################
#initialization#
################
sense = SenseHat()
sense.clear()

#Images
path = os.getcwd()+'/images/'
print(path)
images = [path+i for i in os.listdir(path)]
images = list(filter(match,images))

#Data
pressure = sense.get_pressure()
temp = sense.get_temperature()
hum = sense.get_humidity()

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
#Check of required conditions 
#Temperature: 18.3-26.7 Celsius
#Pressure: 979-1027 millibars
#Humidity: around 60%

###################
# Intro Animation #
###################
try:
    sense.show_message("Hello")
    #show logo
    show_logo(images)
    sense.clear()

    ###########
    # Process #
    ###########
    sense.show_message("Menu")
    while True:
        display(sense,selection)
        event = sense.stick.wait_for_event()
        if event.action == "pressed":
            if event.direction == "middle":
                if execute(sense, selection,images):
                    break
            else:
                selection = move(selection, event.direction)
    sense.clear(
except:
    print("Something went wrong")
    sense.clear()

