import os

NORMAL = " -v lobsang"
HIGH = " -v lobsang-high"
MONO = " -v lobsang-mono"
DEEP = " -v lobsang-deep"
CLEAR = " -v lobsang-clear"
VOICE = NORMAL

SPEED = " -s 170"

VOLUME = " -a 40"

def say(speech):
	os.system("espeak"+ VOICE + SPEED + VOLUME +" '"+ str(speech) +" ' 2>> errors.txt &")

def volume(vol):
	global VOLUME
	VOLUME = " -a "+ str(vol)

def speed(spd):
	global SPEED
	SPEED = " -s "+ str(spd)

def voice(vce):
	global VOICE
	VOICE = vce
