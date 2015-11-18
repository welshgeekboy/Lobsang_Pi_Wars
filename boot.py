#!/usr/bin/env python

import Termcol
import subprocess
import os
import sys
from time import sleep
import Serial
import Lobsang

if not Lobsang.gpio_access:
	#print "boot: GPIO access denied."
	sys.exit(16)

import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.OUT)
GPIO.output(4, False)

number_of_offline_systems = 0
binary_offline_flag = 0 # 0b001 (1) == duino offline, 0b011 (3) == oled and duino offline, 0b100 (4) == camera offline etc

oled_offline = False
duino_offline = False
camera_offline = False

Termcol.info("Checking Lobsang's systems")

Termcol.printf("Checking RasPiO Duino")

if Lobsang.duino.online():
	Termcol.ok("Checking RasPiO Duino")
else:
	reply = ""
	duino_online = False
	Lobsang.duino.reset()
	sleep(0.1)
	Serial.Serial().write("OK?")
	for i in range(0, 20):
		reply += Serial.Serial().read()
		if "DUINO-OK" in reply:
			Termcol.ok("Checking RasPiO Duino")
			print "Had to reset Duino to get response."
			duino_online = True
			break
	if not duino_online:
		Termcol.fail("Checking RasPiO Duino")
		duino_offline = os.system("sudo avrdude -q -q -p m328p -c gpio -P gpio 2> /tmp/avrdude_duino_output_dump")
		if duino_offline == 0 and reply == "":
			Termcol.warning("Duino connected, but core.ino may not be uploaded! Duino is not responding.")
		elif duino_offline == 0 and reply != "":
			Termcol.warning("Duino connected but is not responding correctly. Received: '%s'" %reply)
		elif duino_offline != 0:
			Termcol.warning("Duino not connected")
			print "avrdude: Exited with code %i." %duino_offline
		duino_offline = True
		number_of_offline_systems += 1


Termcol.printf("Testing OLED display")
try:
	Lobsang.oled.command(Lobsang.oled.on)
except IOError:
	oled_offline = True
finally:
	if oled_offline:
		Termcol.fail("Testing OLED display")
		print "Check wiring?"
		number_of_offline_systems += 1
	else:
		Termcol.ok("Testing OLED display")


Termcol.printf("Checking if RasPiCam is connected")
camera_offline = os.system("raspistill -t 1 2> /tmp/dump")
if camera_offline == 0:
	Termcol.ok("Checking if RasPiCam is connected")
else:
	Termcol.fail("Checking if RasPiCam is connected")
	print "Check ribbon cable?"
	camera_offline = True
	number_of_offline_systems += 1

if number_of_offline_systems == 0:
	Termcol.boot("Lobsang booted successfully. All systems online.")
else:
	if number_of_offline_systems == 1:
		error_plural_singular = "error"
	else:
		error_plural_singular = "errors"
	Termcol.boot("Lobsang partially booted: "+ str(number_of_offline_systems) +" "+ error_plural_singular +".")
	
	if duino_error:
		binary_offline_flag += 1
		Termcol.warning("Duino offline")
	if oled_offline:
		binary_offline_flag += 2
		Termcol.warning("OLED display offline")
	if camera_offline:
		binary_offline_flag += 4
		Termcol.warning("Camera offline")

sys.exit(binary_offline_flag)

