import serial

SERNAME = "/dev/ttyAMA0"
IDLE=0; SEND=1; RECEIVE=1

def b2s(msg):
	'''Convert and return received serial bytes $msg to string. If byte is not decodable, return question mark'''
	try:
		return bytes.decode(msg)
	except UnicodeDecodeError:
		return "?"
def s2b(msg):
	'''Convert string $msg to bytes and return'''
	return bytearray(msg, "ascii")

class Serial():
	'''Class for communication with Duino (or other serial device)'''
	def __init__(self, prt=SERNAME):
		'''Prepares class. Runs on calling the class'''
		self.ser = serial.Serial(prt)
		self.state = IDLE

	def __enter__(self):
		return self
	
	def write(self, msg):
		'''Send string $msg to serial device'''
		if self.state == IDLE and self.ser.isOpen():
			self.state = SEND
			self.ser.write(s2b(msg))
			self.state = IDLE
	
	def flush(self):
		'''Ought to remove all data in serial buffer. TODO: make sure it works properly'''
		if self.state == IDLE and self.ser.isOpen():
			self.state = RECEIVE
			while self.ser.inWaiting() > 0:
				self.ser.read(1)
			self.state = IDLE
	
	def receive(self, timeout=0.2, terminate="\r\n"):
		'''Reads serial buffer in an infinite loop until it finds terminating char(s) then returns buffer string'''
		message = ""
		if self.state == IDLE and self.ser.isOpen():
			self.state = RECEIVE
			self.ser.timeout = timeout
			while self.state == RECEIVE:
				echovalue = ""
				while self.ser.inWaiting() > 0:
					echovalue += b2s(self.ser.read(1))
				message += echovalue
				if terminate in message:
					self.state = IDLE
			return message
	
	def read(self):
		'''Reads buffer string at moment of function call (doesn't wait for new data)'''
		message = ""
		timeout = 1
		self.ser.timeout = timeout
		if self.state == IDLE and self.ser.isOpen():
			self.state = RECEIVE
			while self.ser.inWaiting() > 0:
				message += b2s(self.ser.read(1))
			self.state = IDLE
			return message
	
	def __exit__(self, type, value, traceback):
		'''Runs on program exit, eg. KeyboardInterrupt'''
		self.ser.close()
