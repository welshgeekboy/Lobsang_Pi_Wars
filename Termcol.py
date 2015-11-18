#!/usr/bin/env python

import subprocess

# variables for printing colour to the terminal
#HEADER = "\033[95m"
OK = "\033[32m"
INFO = "\033[36m"
WARNING = "\033[33m"
FAIL = "\033[31m"
BOOT = "\033[34;1m"
#BOLD = "\033[1m"
#UNDERLINE = "\033[4m"
ENDC = "\033[0m"

def printf(msg):
	msg = "[ .. ] " + str(msg) + "...\r"
	subprocess.call(["printf", msg])
	
def ok(msg):
	msg = "[ "+ OK +"ok"+ ENDC +" ] "+ msg +"...done."
	subprocess.call(["echo", "-e", msg])

def info(msg):
	msg = "["+ INFO +"info"+ ENDC +"] "+ msg
	subprocess.call(["echo", "-e", msg])

def warning(msg):
	msg = "["+ WARNING +"warn"+ ENDC +"] "+ msg
	subprocess.call(["echo", "-e", msg])

def fail(msg):
	msg = "["+ FAIL +"fail"+ ENDC +"] "+ msg +"...failed!"
	subprocess.call(["echo", "-e", msg])

def boot(msg):
	msg = "["+ BOOT +"boot"+ ENDC +"] "+ msg
	subprocess.call(["echo", "-e", msg])

def test_escape_code(colcode):
	subprocess.call(["echo", "-e", colcode +"This is an escape code colour test."+ ENDC])

def test_number(colnum):
	if colnum != 12:
		subprocess.call(["echo", "-e", "\033["+ str(colnum) +"mThe colour number is "+ str(colnum) + ENDC])
	else:
		print "Cannot use code 12: f**ks up screen!"

def test_two_numbers(num1, num2):
	if num1 != 12 and num2 != 12:
		subprocess.call(["echo", "-e", "\033["+ str(num1) +";"+ str(num2) +"mThe colour numbers are "+ str(num1) +":"+ str(num2) + ENDC])
	else:
		print "Cannot use code 12: f**ks up screen!"

def reset():
	subprocess.call("reset")
