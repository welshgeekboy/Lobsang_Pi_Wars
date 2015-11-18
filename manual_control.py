import pygame
import sys
import time
from pygame.locals import *
import Lobsang

Lobsang.begin()

fps = 50
LMS = 0
RMS = 0

fwd = False
bkd = False
lft = False
rgt = False
stp = False

last_command = (fwd, bkd, lft, rgt, stp)
pygame.init()
DISPLAYSURF = pygame.display.set_mode((1280, 800))
pygame.display.set_caption('Lobsang Manual Control')
clock = pygame.time.Clock()

Lobsang.oled.clear_buffer()
Lobsang.oled.write("Manual Ctrl", pos=(0, 0), size=16)
Lobsang.oled.write("Awaiting instructions...", pos=(0, 24), size=8)
Lobsang.oled.refresh()

old_time = time.time()
total_loops = 0

try:
	start_time = time.time()
	while True: # main game loop
		for event in pygame.event.get():
			if event.type == KEYDOWN:
				if event.key == K_w:
					fwd = True
				elif event.key == K_a:
					lft = True
				elif event.key == K_s:
					bkd = True
				elif event.key == K_d:
					rgt = True
				elif event.key == K_SPACE:
					stp = True
				elif event.key == K_t:
					words = raw_input("What to say? ")
					Lobsang.voice.say(str(words))
				LMS = min(16, LMS)
				LMS = max(-16, LMS)
				RMS = min(16, RMS)
				RMS = max(-16, RMS)
			if event.type == KEYUP:
				if event.key == K_w:
					fwd = False
				elif event.key == K_a:
					lft = False
				elif event.key == K_s:
					bkd = False
				elif event.key == K_d:
					rgt = False
				elif event.key == K_SPACE:
					stp = False
			if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
				Lobsang.wheels.both(0, ramped=False)
				Lobsang.oled.clear_buffer()
				Lobsang.oled.write("Halting Manual mode.")
				print "Manual Control: loop ran for %i seconds or %i times, with average time per loop = %fs" %(int(time.time() - start_time), total_loops, (time.time() - start_time) / total_loops)
				clock.tick(2)
				pygame.quit()
				Lobsang.oled.clear()
				sys.exit()
			#Lobsang.oled.refresh(blackout=False)
		LMS = 0
		RMS = 0
		if not True in (fwd, bkd, lft, rgt):
			stp = True
		else:
			stp = False
		if fwd:
			LMS += 10
			RMS += 10
		if bkd:
			LMS -= 10
			RMS -= 10
		if lft:
			LMS -= 7
			RMS += 9
		if rgt:
			LMS += 9
			RMS -= 7
		elif stp:
			LMS = 0
			RMS = 0
		if (fwd, bkd, lft, rgt, stp) != last_command: # if any of the commands have changed, update the motor speeds
			Lobsang.wheels.both(left_speed=LMS, right_speed=RMS, ramped=True)
			last_command = (fwd, bkd, lft, rgt, stp)
	
		total_loops += 1
		clock.tick(fps)
except Exception as e:
	print e
	print "Manual Control: loop ran for %i seconds or %i times, with average time per loop = %fs" %(int(time.time() - start_time), total_loops, (time.time() - start_time) / total_loops)
