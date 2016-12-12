#!/usr/bin/env python

import signal

try:
    import pygame
except ImportError:
    exit("This script requires the pygame module\nInstall with: sudo pip install pygame")

import explorerhat


print("""
Turns your Explorer HAT into a magical story telling clothes line!

Very rough prototype, attach a crocodile clip to some conctuctive fabric one end 
and the brass explorerhat contacts the other.
""")

LEDS = [4, 17, 27, 5]

samples = [
    '../sounds/hit.wav',
    '../sounds/thud.wav',
    '../sounds/clap.wav',
    '../sounds/crash.wav',
    '../sounds/story.wav',
    '../sounds/story.wav',
    '../sounds/story.wav',
    '../sounds/story.wav',
]

pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.mixer.init()
pygame.mixer.set_num_channels(16)

sounds = []
for x in range(8):
    sounds.append(pygame.mixer.Sound(samples[x]))


def handle(ch, evt):
    if ch > 4:
        led = ch - 5
    else:
        led = ch - 1
    if (evt == 'press' and pygame.mixer.get_busy() == False):
        explorerhat.light[led].fade(0, 100, 0.1)
        sounds[ch - 1].play(loops=0)
        name = samples[ch - 1].replace('../sounds/','').replace('.wav','')
        print("{}!".format(name.capitalize()))
    else:
        explorerhat.light[led].off()


explorerhat.touch.pressed(handle)
explorerhat.touch.released(handle)

explorerhat.light.green.blink(1, 1)


signal.pause()
