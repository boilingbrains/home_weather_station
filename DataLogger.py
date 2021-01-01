#! /usr/bin/python3

#Modules
from sense_hat import SenseHat
import numpy as np
import time
import cv2
import os
import PIL
from PIL import Image
sense = SenseHat()
sense.clear()

#Collect Data
pressure = sense.get_pressure()
dtemp = sense.get_temperature()
hum = sense.get_humidity()

#Check of required conditions 
#Temperature: 18.3-26.7 Celsius
#Pressure: 979-1027 millibars
#Humidity: around 60%


#Display
def match(element):
    return bool(element[len(element)-3:len(element)] == 'png' )
path = os.getcwd()+'/images/'
print(path)
images = [i for i in os.listdir(path)]
images = list(filter(match,images))
print(images)
for i in images:
    print(i)
    #image = cv2.imread(path + i)
    #image = cv2.resize(image,(8,8))
    image = Image.open(path+i)
    image = image.resize((8,8),PIL.Image.ANTIALIAS)
    name = "resized"+i
    image.save(name
    sense.load_image(path+name)
    sleep(4)
    #cv2.imshow(i,image)
    #cv2.waitKey(0) 
#cv2.destroyAllWindows()        
sense.clear()
print("voilà")

####
# Intro Animation
####

#show logo
#Menu
#Rd = (255, 0, 0)
#Gn = (0, 255, 0)
#Bl = (0, 0, 255)
#Gy = (128, 128, 128)
#__ = (0, 0, 0)
#
#
#
##Plot
#


#
## Draw the foreground (fg) into a numpy array
#fg = np.array([
#    [Rd, Rd, Rd, __, Gn, Gn, __, __],
#    [__, Rd, __, __, Gn, __, Gn, __],
#    [__, Rd, __, __, Gn, Gn, __, __],
#    [__, Rd, __, __, Gn, __, __, __],
#    [Bl, __, Bl, __, __, Gy, __, __],
#    [Bl, Bl, Bl, __, Gy, __, Gy, __],
#    [Bl, __, Bl, __, Gy, __, Gy, __],
#    [Bl, __, Bl, __, __, Gy, Gy, __],
#    ], dtype=np.uint8)
## Mask is a boolean array of which pixels are transparent
#mask = np.all(fg == __, axis=2)
#
#def display(hat, selection):
#    # Draw the background (bg) selection box into another numpy array
#    left, top, right, bottom = {
#        'T': (0, 0, 4, 4),
#        'P': (4, 0, 8, 4),
#        'Q': (4, 4, 8, 8),
#        'H': (0, 4, 4, 8),
#        }[selection]
#    bg = np.zeros((8, 8, 3), dtype=np.uint8)
#    bg[top:bottom, left:right, :] = (255, 255, 255)
#    # Construct final pixels from bg array with non-transparent elements of
#    # the menu array
#    hat.set_pixels([
#        bg_pix if mask_pix else fg_pix
#        for (bg_pix, mask_pix, fg_pix) in zip(
#            (p for row in bg for p in row),
#            (p for row in mask for p in row),
#            (p for row in fg for p in row),
#            )
#        ])
#
#def execute(hat, selection):
#    if selection == 'T':
#        hat.show_message('Temperature: %.1fC' % hat.temp, 0.05, Rd)
#    elif selection == 'P':
#        hat.show_message('Pressure: %.1fmbar' % hat.pressure, 0.05, Gn)
#    elif selection == 'H':
#        hat.show_message('Humidity: %.1f%%' % hat.humidity, 0.05, Bl)
#    else:
#        return True
#    return False
#
#def move(selection, direction):
#    return {
#        ('T', DIRECTION_RIGHT): 'P',
#        ('T', DIRECTION_DOWN):  'H',
#        ('P', DIRECTION_LEFT):  'T',
#        ('P', DIRECTION_DOWN):  'Q',
#        ('Q', DIRECTION_UP):    'P',
#        ('Q', DIRECTION_LEFT):  'H',
#        ('H', DIRECTION_RIGHT): 'Q',
#        ('H', DIRECTION_UP):    'T',
#        }.get((selection, direction), selection)
#
#hat = SenseHat()
#selection = 'T'
#while True:
#    display(hat, selection)
#    event = hat.stick.wait_for_event()
#    if event.action == ACTION_PRESSED:
#        if event.direction == DIRECTION_MIDDLE:
#            if execute(hat, selection):
#                break
#        else:
#            selection = move(selection, event.direction)
#hat.clear()
#

