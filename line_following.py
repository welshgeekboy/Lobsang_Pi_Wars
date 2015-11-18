#!/usr/bin/env python

# line_following.py - Sixth attempt at line following.
# Now works pretty well!
#
# Created Nov 2015 by Finley Watson

print "Line Following: Initialising."

import Lobsang
Lobsang.oled.write("Line Following: Initialising.")
Lobsang.oled.refresh()

import time
import os
import sys
import pygame
from pygame.locals import *

DEBUG = False
SHOW_MAP = False

if DEBUG: print "Line Following: Debug is on. Will print program info."
if SHOW_MAP: print "Line Following: Map is on. Will print line map each loop."

black    = 1
white    = 0
map      = [white, white, white]
left     = [black, white, white]
left_90  = [black, black, white]
middle   = [white, black, white]
right    = [white, white, black]
right_90 = [white, black, black]
blank    = [white, white, white]

fps = 50
running = True

line_buffer = [[blank, 0.0], [blank, 0.0], [blank, 0.0], [blank, 0.0], [blank, 0.0]] # remembers up to five line changes ago, plus timestamps for each change

total_loops = 0

direction = "stop"
old_direction = "stop"

pygame.init()
display = pygame.display.set_mode((1280, 800))
pygame.display.set_caption("Line Following Program")

old_time = time.time()
t1 = time.time()

if not Lobsang.gpio_access:
	raise PermissionError("Use sudo prefix. No GPIO acces.")

Lobsang.begin(splashscreen=False)
time.sleep(1)
Lobsang.head.aim(1500, 1800)

print "Line Following: Running main loop."
if DEBUG: os.system("printf 'Motors: stop for '")

def update_line_buffer(line_data):
	for i in range(len(line_buffer) - 1, 0, -1):
		line_buffer[i] = line_buffer[i - 1]
	line_buffer[0][0] = line_data
	line_buffer[0][1] = time.time()

def line_velocity(dir, tim):
	# return velocity of line compared to a stationary sensor. right is positive velocity
	# requires $tim as last line pos data timestamp, and $dir which is 1 (right) or -1 (left)
	# 0.023 is the distance between sensors in meters. speed = distance / time
	speed_m_s = (int(0.023 / (time.time() - tim) * 1000.0) / 1000.0) * dir
	return speed_m_s

try:
	start = time.time()
	temp_time = time.time()
	while True:
		time.sleep(1.0 / fps)
		temp_time = time.time()
		total_loops += 1
		map = Lobsang.sensors.line_map() # poll IR line following sensors through serial to duino
		if SHOW_MAP: print "Line map:", map; print "Line buffer:", line_buffer; print # print the response
		
		for event in pygame.event.get():
			if event.type == KEYDOWN:
				if event.key == K_SPACE:
					running = not running
					if running:
						Lobsang.duino.enable()
						time.sleep(0.5)
						if direction == "forward":
							Lobsang.wheels.both(13)
						elif direction == "left":
							Lobsang.wheels.both(6, 16)
						elif direction == "right":
							Lobsang.wheels.both(16, 6)
					else:
						Lobsang.duino.disable()
			if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
				Lobsang.duino.disable()
				Lobsang.oled.write("Halting line follow code", pos=(0, 24))
				Lobsang.oled.refresh()
				pygame.quit()
				print "\r\nLine Following: Exiting"
				print "Line Following: main loop ran for %s seconds or %i times, with average time per loop: %fs" %(str(int((time.time() - start) * 1000.0) / 1000.0), total_loops, (time.time() - start) / total_loops)
				time.sleep(1)
				Lobsang.quit(screensaver=False)
				sys.exit()
		if running:
			if map != line_buffer[0][0]: # if the line map has changed
				update_line_buffer(map)
				if map == middle: # line is under centre sensor
					direction = "forward"
					Lobsang.wheels.both(13)
				elif map == left or map == left_90: # line is under the left sensor
					direction = "left"
					Lobsang.wheels.both(6, 16) # line is under the right sensor
				elif map == right or map == right_90:
					direction = "right"
					Lobsang.wheels.both(16, 6)
				elif map == blank: # line is under none of the sensors- either between the sensors so they don't see it, or to the left or right of the sensor as a whole
					if direction == "left": # if the line is not under the sensor and the robot is turning left, make it turn sharper as it is understeering
						Lobsang.wheels.both(-4, 16)
					elif direction == "right": # if the line is not under the sensor and the robot is turning right, make it turn sharper as it is understeering
						Lobsang.wheels.both(16, -4)
				
				if DEBUG and direction != old_direction: # if $DEBUG flag is set to True and the direction of the motors have changed, print the change and the time spent in the previous direction
					os.system("printf '%fs\r\nMotors: %s for '" %(((time.time() - old_time) * 10000) / 10000.0, direction)) # print time taken for last motor directions, then newline and print next direction
					old_direction = direction
					old_time = time.time()

except KeyboardInterrupt:
	Lobsang.duino.disable()
	Lobsang.oled.write("Halting IR line follow code", pos=(0, 24))
	Lobsang.oled.refresh()
	print "\r\nLine Following: Exiting"
	print "Line Following: main loop ran for %s seconds or %i times, with average time per loop: %fs" %(str(int((time.time() - start) * 1000.0) / 1000.0), total_loops, (time.time() - start) / total_loops)
	time.sleep(1)
	Lobsang.quit(screensaver=False)

except Exception as e:
	Lobsang.duino.disable()
	print
	print "\r\nError in line follow code: %s. Halting." %e
	Lobsang.oled.write("Error in line follow code. Halting.", pos=(0, 24))
	Lobsang.oled.refresh()
	time.sleep(2)
	Lobsang.quit(screensaver=False)

print "exit"
