#!/usr/bin/env python

# piwars_menu.py - A way of calling the different
# scripts for each challenge without looing at a
# standard screen. Displays info on the OLED and
# runs piwars scripts which on exit allow this
# script to keep running. Use number keys to select
# the script you want to run and ESC to exit program.
#
# Created Nov 2015 by Finley Watson

print "Piwars Menu: Initialising."
import time

# Use these as false boolean variables until they are filled by the library (using "import").
# That way the "except:" statement at the bottom knows if the libraries are imported yet.
pygame = False
Lobsang = False

# Put everything in a try statement so if the user quits the menu while it is loading (with ^C) then it exits nicely.
try:
	# My libraries
	import Lobsang
	import sys
	Lobsang.oled.write("Starting Piwars Menu.")
	if not Lobsang.gpio_access:
		Lobsang.oled.clear()
		sys.exit()
	Lobsang.oled.refresh()
	# Other libraries
	time.sleep(2) # Give the user a chance to use KeyboardInterrupt if they want to, before pygame creates its window.
	import pygame
	from pygame.locals import *
	import os
	
	fps = 10 # Number of checks or loop cycles per seond
	menu_position = 0 # OLED menu position (0 - 3)
	# All the options that are supported by this script. The spaces make the text appear right-alined (purely aesthetic!).
	menu_options = ["1:                           Line following", "2:                       Manual control", "3:               Drag race control", "4:                          Proximity test", "5:                Skittles challenge", "6:                   Three point turn", "ESC:              Exit Piwars Menu"]
	
	# Set up pygame (for a HDMIPi screen so 1280x800 but size does not matter).
	pygame.init()
	display = pygame.display.set_mode((1280, 800))
	pygame.display.set_caption('Piwars Program Select Menu') # This only shows if you are using the GUI, not the terminal.
	clock = pygame.time.Clock()
	
	def render_menu(menu_pos):
		'''Displays the menu on the OLED at the position
		   set by up/down keys. Not all of the menu
		   is visible at any one time. This scrolls it.'''
		Lobsang.oled.clear_buffer()
		Lobsang.oled.write("  PiWars Menu", size=16) # Write the title at the top.
		for i in range(menu_pos, menu_position + 4): # From top of scrolled menu to bottom of scrolled menu, write each option that is visible.
			Lobsang.oled.write(menu_options[i], size=8)
		Lobsang.oled.refresh(blackout=False) # Refresh the screen to display the new data but don't blank the screen while it's being updated- this makes transition smoother.
	
	render_menu(0) # Display the menu at the automatic starting point- at the top.
	while True: # Loop indefinitely, waiting to run the piwars programs.
		for event in pygame.event.get():
			if event.type == KEYDOWN:
				if event.key == K_1:
					print "Piwars Menu: Running line follow code..."
					pygame.quit() # Halt the pygame window to stop a weird freeze when more than one pygame window opens in the terminal, and so you can see any terminal messages printed by script run below.
					os.system("sudo python line_following.py")
					print "Piwars Menu: Finished running line follow code. Continuing menu."
					render_menu(menu_position)
					pygame.init() # After the script has finished, restart the pygame window to continue getting keyboard events.
					display = pygame.display.set_mode((1280, 800))
				
				elif event.key == K_2:
					print "Piwars Menu: Running manual control code..."
					pygame.quit()
					os.system("sudo python manual_control.py")
					print "Piwars Menu: Finished running manual control code. Continuing menu."
					render_menu(menu_position)
					pygame.init()
					display = pygame.display.set_mode((1280, 800))
				
				elif event.key == K_3:
					print "Piwars Menu: Running straight line speed test manual control code..."
					pygame.quit()
					os.system("sudo python drag_race.py")
					print "Piwars Menu: Finished running straight line speed test manual control code. Continuing menu."
					render_menu(menu_position)
					pygame.init()
					display = pygame.display.set_mode((1280, 800))
				
				elif event.key == K_4:
					print "Piwars Menu: Running proximity alert code..."
					pygame.quit()
					os.system("sudo python proximity_alert.py")
					print "Piwars Menu: Finished running proximity alert code. Continuing menu."
					pygame.init()
					display = pygame.display.set_mode((1280, 800))
				
				elif event.key == K_5:
					print "Piwars Menu: Running skittles challenge code..."
					pygame.quit()
					os.system("sudo python skittles_challenge.py")
					print "Piwars Menu: Finished running skittles code. Continuing menu."
					render_menu(menu_position)
					pygame.init()
					display = pygame.display.set_mode((1280, 800))
				
				elif event.key == K_6:
					print "Piwars Menu: Running three point turn code..."
					pygame.quit()
					os.system("sudo python three_point_turn.py")
					print "Piwars Menu: Finished running three point turn code. Continuing menu."
					render_menu(menu_position)
					pygame.init()
					display = pygame.display.set_mode((1280, 800))
				
				elif event.key == K_UP: # Move up the menu one line.
					if menu_position > 0:
						menu_position -= 1
						render_menu(menu_position)
				
				elif event.key == K_DOWN: # Move down the menu one line.
					if menu_position < 3:
						menu_position += 1
						render_menu(menu_position)
				
				if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE): # Exit this program (ESC (or close button in GUI) pressed).
					print "Piwars Menu: Halting."
					Lobsang.duino.disable()
					Lobsang.oled.clear_buffer()
					Lobsang.oled.write("Halting Piwars Menu.")
					Lobsang.oled.refresh()
					pygame.quit()
					Lobsang.oled.clear()
					sys.exit()
		clock.tick(fps)
except KeyboardInterrupt:
	print "\r\nPiwars Menu: Halting."
	if Lobsang and Lobsang.gpio_access:
		Lobsang.duino.disable()
		Lobsang.oled.clear_buffer()
		Lobsang.oled.write("Halting Piwars Menu.")
		Lobsang.oled.refresh()
	if pygame: pygame.quit()
	elif Lobsang: time.sleep(0.5)
	if Lobsang: Lobsang.oled.clear()
# EXIT
