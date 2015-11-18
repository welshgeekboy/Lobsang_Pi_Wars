#!/usr/bin/env python
#
# autorun.py: a script to check if robot systems are
# all online. If they are, then it will run the main
# program (currently piwars_menu.py) if they are not
# then wait for a login or access key (correct usb
# stick). To disable automatic running of this file
# once per boot on tty1 at boot, edit the file 
# /etc/rc.local and comment out the correct line.

print "Auto Run: Initialising."

# my libraries
import Oled
try: # We have not yet checked if the OLED is connected, so only "try:" to do this.
	Oled.write("Starting Auto Run.")
	Oled.refresh()
except:
	pass
import Padlock
# other python libraries
import random
import time
import subprocess
import os
import sys

oled_online = True
safe =  True


# Run boot.py, a system checkup script.
boot_errors = subprocess.call(["python", "boot.py"])

# Script exit code gives info about systems: 0 is all online,
# +4 == camera offline, +2 == oled offline, +1 == duino offline.
# So an error code of 6 == oled and cam offline but error of
# 5 == camera and duino offline. This data is split into each part below.
# If no GPIO access then boot.py always exits with code 16.
if boot_errors > 0: # There ARE errors
	if boot_errors == 16:
		print "Auto Run: No GPIO access."
		sys.exit()
	if boot_errors >= 2:
		boot_errors -= 2
		oled_online = False
	if boot_errors >= 1:
		boot_errors -= 1
		safe = False
	if boot_errors != 0:
		print "Auto Run: Error checking for boot errors. Wrong error code returned from boot.py? Error code == %i" %boot_errors
if safe:
	if oled_online:
		Oled.clear_buffer()
		Oled.render("betatall.png", pos=(32, 0))
		Oled.write("Auto Run: All systems online.", pos=(0, 24))
		Oled.refresh()
		Oled.command(Oled.on)
	print "Auto Run: Success! System is stable."
	os.system("sudo python piwars_menu.py")

else:
	print "Auto Run: Cannot boot Lobsang!"
	if oled_online:
		Oled.render("betatall.png", pos=(32, 0))
		Oled.write("Auto Run: Cannot boot Lobsang!", pos=(0, 24))
		Oled.refresh()
		Oled.command(Oled.on)

# runs after piwars_menu.py exits / on unstable system error
print "Auto Run: Please login or use USB key."
attempt = Padlock.attempt_unlock()
if attempt == Padlock.unlocked:
	print "Auto Run: System access gained."
	print "Auto Run: Exit program."
else:
	print "Auto Run: Access failed. Sleeping forever..."
	while True: # this cannot be halted!!! Pi reboot needed.
		try:
			time.sleep(1000)
		except:
			pass
# EXIT
