#!/usr/bin/env python
# James Beecroft and Harry Leversidge
import signal
from sys import exit

try:
    import pygame
except ImportError:
    exit("This script requires the pygame module\nInstall with: sudo pip install pygame")

import explorerhat
import random


print("""
This code helps you turn a bucket into a cauldron.

Press CTRL+C to exit.
""")

LEDS = [4, 17, 27, 5]

samples = [
    #'sounds/342474__newagesoup__titleflight-bubbling-liquid-splatter.wav',
   # 'sounds/347883__garygit__dia-chichra.wav',
    '../sounds/41617__noisecollector__witchtoycackle.wav',
    '../sounds/79140__razzvio__blowing-bubbles.wav',
   
]

pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.mixer.init()
pygame.mixer.set_num_channels(16)


sounds = []
for x in range(len(samples)):
    sounds.append(pygame.mixer.Sound(samples[x]))


def handle(ch, evt):
    if ch > 4:
        led = ch - 5
    else:
        led = ch - 1
    if evt == 'press':
        explorerhat.light[led].fade(0, 100, 0.1)
        sounds[random.randint(0,len(samples)-1)].play(loops=0)
        #name = samples[ch - 1].replace('sounds/','').replace('.wav','')
        #print("{}!".format(name.capitalize()))
    else:
        explorerhat.light[led].off()


explorerhat.touch.pressed(handle)
explorerhat.touch.released(handle)

def handle_input(pin):
    print(pin.name, pin.read())
    sounds[random.randint(0,len(samples)-1)].play(loops=0) 

explorerhat.input.on_high(handle_input,2000)
signal.pause()
