#!/usr/bin/env python
# james beecroft and Harry leversidge
# Mr Eggleton

import signal
from sys import exit

try:
    import pygame
except ImportError:
    exit("This script requires the pygame module\nInstall with: sudo pip install pygame")

import explorerhat

import time
from colorsys import hsv_to_rgb
import random
from mote import Mote

samples = [
    '../sounds/62967__robinhood76__ab001-chimes-on-wind.wav'
]

pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.mixer.init()
pygame.mixer.set_num_channels(16)

sounds = []
for x in range(len(samples)):
    sounds.append(pygame.mixer.Sound(samples[x]))

print("""Fairy Ring

Press Ctrl+C to exit.
""")

mote = Mote()

mote.configure_channel(1, 16, False)
mote.configure_channel(2, 16, False)
mote.configure_channel(3, 16, False)
mote.configure_channel(4, 16, False)


sounds[0].play(loops=-1)
sounds[0].set_volume(0)

iStrength = 0;
iStep = 10;

def handle(ch, evt):	
    global iStrength	
    if evt == 'press':
        sounds[0].play(loops=0)
        if ch > 4:
			if (iStrength > 0) :
				iStrength -= iStep
			
        else:
			if (iStrength < 250) :
				iStrength += iStep
        
        fVolume = float(iStrength)/250.0
        print (iStrength, fVolume)
        sounds[0].set_volume(fVolume)
		
explorerhat.touch.pressed(handle)
explorerhat.touch.released(handle)       
  

try:
    while True:
        h = time.time() * 50
        for channel in range(4):
            for pixel in range(16):
                hue = (h + (channel * 64) + (pixel * 4)) % 360
                r, g, b = [int(c * iStrength) for c in hsv_to_rgb(hue/360.0, 1.0,  random.random()

)]
                mote.set_pixel(channel + 1, pixel, r, g, b)
        mote.show()
        time.sleep(0.05)

except KeyboardInterrupt:
    mote.clear()
    mote.show()

signal.pause()
