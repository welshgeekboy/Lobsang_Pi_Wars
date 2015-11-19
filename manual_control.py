#!/usr/bin/env python
#
# manual_control.py-  script to allow the user to
# control the robot with the "W A S D" keys. Uses
# pygame to get key presses,  and allows  keys to
# be pressed at the same time for greater control
# so you can drive left,  left and forward,  only
# forward, right and forward etc.  ESC  to  quit.
#
# Created Nov 2015 by Finley Watson.

print "Manual Control: Initialising."

# Import all the libraries we need.
import Lobsang
import pygame
import sys
import time
from pygame.locals import *

# Give feedback on the oled.
Lobsang.oled.write("Starting Manual Control.")
Lobsang.oled.refresh()
Lobsang.begin(splashscreen=False)

# All the variables needed.
loops_per_second = 50
left_motor_speed = 0
right_motor_speed = 0

forward = False
backward = False
left = False
right = False

# Set up pygame
pygame.init()
DISPLAYSURF = pygame.display.set_mode((1280, 800))
pygame.display.set_caption('Lobsang Manual Control')
clock = pygame.time.Clock()

# Print the interface info on the oled.
Lobsang.begin(splashscreen=False)
Lobsang.oled.clear_buffer()
Lobsang.oled.write("Manual Ctrl", pos=(0, 0), size=16)
Lobsang.oled.write("Control with W, A, S, D keys.")
Lobsang.oled.write("Press ESC to quit.")
Lobsang.oled.refresh()

# Calibrate the motor speeds to run in an approximately straight line.
Lobsang.wheels.calibrate_speeds(-0.8)

old_time = time.time()
total_loops = 0

try: # Put the main loop in a try statement to catch errors and stop the robot before exiting scipt.
	start_time = time.time()
	while True: # Loop indefinitely
		for event in pygame.event.get(): # Search through events for keys we need to respond to
			if event.type == KEYDOWN:
				if event.key == K_w:
					forward = True
				elif event.key == K_a:
					left = True
				elif event.key == K_s:
					backward = True
				elif event.key == K_d:
					right = True
			if event.type == KEYUP:
				if event.key == K_w:
					forward = False
				elif event.key == K_a:
					left = False
				elif event.key == K_s:
					backward = False
				elif event.key == K_d:
					right = False
			if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
				current_time = time.time()
				Lobsang.wheels.both(0, ramped=False)
				Lobsang.oled.clear_buffer()
				Lobsang.oled.write("Halting Manual mode.") 
				print "Manual Control: main loop ran for %s seconds or %i times, with average time per loop of %fs and %s loops per second." %(str(int((current_time - start_time) * 100.0) / 100.0), total_loops, (current_time - start_time) / total_loops, str(int(1 / ((current_time - start_time) / total_loops) * 100.0) / 100.0))
				print "Manual Control: Halting."
				clock.tick(2)
				pygame.quit()
				Lobsang.oled.clear()
				sys.exit()
		left_motor_speed = 0
		right_motor_speed = 0
		if forward and not True in (left, right, backward): # Only forward key pressed
			left_motor_speed = 16
			right_motor_speed = 16
			calibration = -0.15
		elif backward and not True in (forward, left, right): # Only backward key pressed
			left_motor_speed = -16
			right_motor_speed = -16
			calibration = -0.15
		elif left and not True in (forward, right, backward): # Only left key pressed
			left_motor_speed = -9
			right_motor_speed = 9
		elif right and not True in (forward, left, backward): # Only right key pressed
			left_motor_speed = 9
			right_motor_speed = -9
		elif forward and left and not right: # Both forward and left keys pressed, but not right. 
			left_motor_speed = 4
			right_motor_speed = 16
		elif forward and right and not left: # Both forward and right keys pressed, but not left.
			left_motor_speed = 16
			right_motor_speed = 4
		elif backward and left and not right: # Both backward and left keys pressed, but not right.
			left_motor_speed = -16
			right_motor_speed = -4
		elif backward and right and not left: # Both backward and right keys pressed, but not left.
			left_motor_speed = -4
			right_motor_speed = -16
		else:
			left_motor_speed = 0
			right_motor_speed = 0
		
		Lobsang.wheels.both(left_motor_speed, right_motor_speed)
		total_loops += 1
		clock.tick(loops_per_second)
except Exception as e:
	Lobsang.wheels.both(0, ramped=False)
	Lobsang.oled.clear_buffer()
	Lobsang.oled.write("Halting Manual Control.")
	print "An error occurred in Manual Control: %s. Halting." %e
	print "Manual Control: loop ran for %i seconds or %i times, with average time per loop = %fs" %(int(time.time() - start_time), total_loops, (time.time() - start_time) / total_loops)
	# Exit
