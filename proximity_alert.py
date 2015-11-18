#!/bin/env python
#
# proximity_alert.py- simple script for Piwars 2015
# to approach a wall and stop as close as I dare
# to it without touching.
#
# Created 2015 by Finley Watson

# My library
import Lobsang

Lobsang.oled.write("Starting Proximity Alert.")
Lobsang.oled.refresh()

# Other libraries
import time
import pygame
import sys
from pygame.locals import *

pygame.init()
display = pygame.display.set_mode((1280, 800))

print_reading_count = 0
cm = 0
running = False
disabled = False

Lobsang.begin(splashscreen=False)
Lobsang.head.aim(1430, 1430)
Lobsang.oled.clear_buffer()
Lobsang.oled.write("Proximity", size=16)
Lobsang.oled.write("Press SPACE to start.", size=8)
Lobsang.oled.refresh(blackout=False)

while True:
	for event in pygame.event.get():
		if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
			Lobsang.oled.clear_buffer()
			Lobsang.oled.write("Halting Proximity Alert.")
			Lobsang.oled.refresh()
			time.sleep(0.5)
			Lobsang.quit(False)
			pygame.quit()
			Lobsang.oled.clear()
			sys.exit()
		elif event.type == KEYDOWN:
			if event.key == K_SPACE:
				running = not running
				if running:
					Lobsang.oled.clear_buffer()
					Lobsang.oled.write("Proximity", size=16)
					Lobsang.oled.write("Press SPACE to stop.", size=8)
					Lobsang.oled.refresh(blackout=False)
					disabled = False
				else:
					Lobsang.oled.clear_buffer()
					Lobsang.oled.write("Proximity", size=16)
					Lobsang.oled.write("Press SPACE to start.", size=8)
					Lobsang.oled.refresh(blackout=False)

	if running:
		cm = Lobsang.sensors.distance()
		if print_reading_count > 2: print cm; print_reading_count = 0
		if cm > 50:
			Lobsang.wheels.both(16)
		elif cm > 20:
			Lobsang.wheels.both(6)
		elif cm > 11:
			Lobsang.wheels.both(0)
		else:
			Lobsang.wheels.both(-5)
	elif not disabled:
		disabled = True
		Lobsang.wheels.both(0)
