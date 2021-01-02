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
#def match(element):
#    return bool(element[len(element)-3:len(element)] == 'png' )

def show_logo(images):
    print(images)
    for i in images:
        print(i)
        sense.load_image(i)
        time.sleep(1)
        
def check_conditions(param,selection,images2):
    #Check of required conditions 
    #Temperature: 18.3-26.7 Celsius
    #Pressure: 979-1027 millibars
    #Humidity: around 60%
    print('ici')
    if selection == 'T':
        if param < 18.3 or param > 26.7:
            sense.load_image(images2[0])
        else:
            sense.load_image(images2[1])
    elif selection == 'P':
        if param < 979 or param > 1027:
            sense.load_image(images2[0])
        else:
            sense.load_image(images2[1])
    elif selection == 'H':
        if param < 60:
            sense.load_image(images2[0])
        else:
            sense.load_image(images2[1])
    
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

def execute(sense,check_conditions, selection,images):
    t = sense.get_temperature_from_pressure()
    p = sense.get_pressure()
    h = sense.get_humidity()
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


################
#initialization#
################
sense = SenseHat()
sense.clear()

#Images
path = os.getcwd()+'/images/'
print(path)
images = [path+'logo/'+i for i in os.listdir(path+'logo/')]
images2 = [path+'conditions/'+i for i in os.listdir(path+'conditions/')]
#images = list(filter(match,images))

#Data
pressure = sense.get_pressure()
temp = sense.get_temperature_from_humidity()
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
        event = sense.stick.wait_for_event()
        if event.action == "pressed":
            if event.direction == "middle":
                if execute(sense,check_conditions, selection,images):
                    break
            else:
                selection = move(selection, event.direction)
    sense.clear()
except:
    #print("Something went wrong")
    sense.clear()

