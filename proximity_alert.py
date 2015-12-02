#!/usr/bin/env python
#
# proximity_alert.py- simple script for Piwars 2015
# to approach a wall and stop as close as I dare to
# it without touching. Uses an ultrasonic and an IR
# line following sensor mounted to detect the wall,
# facing  forwards  instead of down at the  ground.
#
# Created Nov 2015 by Finley Watson

print "Proximity Alert: Initialising."

# Import all libraries needed.
import Lobsang
import time
import pygame
import sys
from pygame.locals import *

# Give feedback on the oled.
Lobsang.oled.write("Starting Proximity Alert.")
Lobsang.oled.refresh()

# All variables needed.

loops_per_second = 50
current_time = 0
total_loops = 0

allowed_to_run = False
disabled = False

cm = 0
use_ultrasonic = True
use_ir = True
finished_approach = False

# What the IR sensor can detect.
white = 0
black = 1

# Set up pygame.
pygame.init()
display = pygame.display.set_mode((1280, 800))
clock = pygame.time.Clock()

# Display interface info on the oled.
Lobsang.begin(splashscreen=False)
Lobsang.wheels.calibrate_speeds(-0.2)
Lobsang.head.aim(1430, 1430)
Lobsang.oled.clear_buffer()
Lobsang.oled.write("Proximity", size=16)
Lobsang.oled.write("Press SPACE to start.")
Lobsang.oled.write("Press ESC to quit.")
Lobsang.oled.refresh(blackout=False)

try: # Put main loop in a try statement to stop the robot and exit cleanly on an Exception.
	start_time = time.time()
	while True: # Loop indefinitely
		clock.tick(loops_per_second) # No need to run as fast as possible
		for event in pygame.event.get(): # Check through events to see if there are key presses we need to respond to.
			if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE): # Exit program
				current_time = time.time()
				Lobsang.oled.clear_buffer()
				Lobsang.oled.write("Halting Proximity Alert.")
				Lobsang.oled.refresh()
				print "Proximity Alert: main loop ran for %s seconds or %i times, with average time per loop of %fs and %s loops per second." %(str(int((current_time - start_time) * 100.0) / 100.0), total_loops, (current_time - start_time) / total_loops, str(int(1 / ((current_time - start_time) / total_loops) * 100.0) / 100.0))
				print "Proximity Alert: Halting"
				time.sleep(0.5)
				Lobsang.quit(screensaver=False)
				pygame.quit()
				sys.exit()
			
			elif event.type == KEYDOWN:
				if event.key == K_SPACE:
					allowed_to_run = not allowed_to_run # Toggle running of program
					if finished_approach:
						allowed_to_run = True
						use_ultrasonic = True
						use_ir = True
						finished_approach = False
					if allowed_to_run:
						Lobsang.oled.clear_buffer()
						Lobsang.oled.write("Proximity", size=16)
						Lobsang.oled.write("Press SPACE to stop.")
						Lobsang.oled.refresh(blackout=False)
						disabled = False
					else:
						Lobsang.oled.clear_buffer()
						Lobsang.oled.write("Proximity", size=16)
						Lobsang.oled.write("Press SPACE to start.")
						Lobsang.oled.refresh(blackout=False)
						Lobsang.wheels.both(0)
		
		if allowed_to_run and not finished_approach: # Self explanatory- good use of variable names! :-)
			if use_ultrasonic: # Wall is still some distance away. Use (rather innaccurate) ultrasonic for rough measurements.
				cm = Lobsang.sensors.distance()
				if cm > 50: # Wall is 50cm+ so full speed ahead!
					Lobsang.wheels.both(16)
				elif cm > 25: # Wall is 49 to 25cm so go more slowly.
					Lobsang.wheels.calibrate_speeds(-0.35)
					Lobsang.wheels.both(6)
				else: # Wall is less than 25cm from the robot- stop checking distance with ultrasound and start using the repositioned line following sensor as an active IR obstacle sensor.
					Lobsang.oled.write("Nearly there...")
					Lobsang.oled.refresh(blackout=False)
					Lobsang.wheels.calibrate_speeds(-0.4)
					Lobsang.wheels.both(5)
					use_ultrasonic = False
			elif use_ir: # Use the line following sensor to detect when the wall is VERY close.
				map = Lobsang.sensors.line_map()
				if white in map: # If the wall is detected by any of the three sensors, stop the robot.
					Lobsang.wheels.both(0)
					while Lobsang.sensors.line_map() != [white, white, white]:
						map = Lobsang.sensors.line_map()
						if map[0] == white and map[2] == black: 
							Lobsang.wheels.left(0)
							Lobsang.wheels.right(4)
						elif map[0] == black and map[2] == white:
							Lobsang.wheels.left(4)
							Lobsang.wheels.right(0)
					Lobsang.wheels.both(0)
					use_ir = False
					Lobsang.oled.clear_buffer()
					Lobsang.oled.write("Proximity", size=16)
					Lobsang.oled.write("Finished approach to wall.")
					Lobsang.oled.write("Press SPACE to restart or ESC to quit.")
					Lobsang.oled.refresh(blackout=False)
					finished_approach = True
		total_loops += 1

except Exception as e:
	print "An error occurred in Proximity Alert: %s. Halting." %e
	Lobsang.oled.clear_buffer()
	Lobsang.oled.write("Halting Proximity Alert.")
	Lobsang.oled.refresh()
	time.sleep(0.5)
	pygame.quit()
	Lobsang.quit(screensaver=False)
	# Exit
