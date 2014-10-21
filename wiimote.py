#!/usr/bin/python
import cwiid
import time

# Connect to the Wii Remote. 

class Wiimote:

	wiimote = ""
	
	def connect(self):
		try:
			print 'Press 1 + 2 on your Wii Remote now ...'
			time.sleep(1)
			self.wiimote = cwiid.Wiimote()
		except RuntimeError:
			self.connect()
	
	def connect_wiimote(self):
		self.connect()

		print 'Wii Remote connected...\n'
		self.wiimote.led = 6
		self.wiimote.rpt_mode = cwiid.RPT_BTN

	def validate_connection(self):
		try:
			self.wiimote.request_status()
		except RuntimeError:
			print "Disconnected - reconnecting"
			self.wiimote = connect_wiimote()

	def connection_fun(self):
		time.sleep(1)
		for i in range(4):
			self.wiimote.rumble = True
			time.sleep(.1)
			self.wiimote.rumble = False
			time.sleep(.1)
		self.wiimote.led = 0
		time.sleep(1)
		for i in [1, 2, 4, 8, 4, 2, 1, 2, 4, 8, 4, 2, 1, 2, 4, 8, 4, 2, 1, 0]:
			self.wiimote.led = i
			time.sleep(.1)
		self.wiimote.led = 6
		self.wiimote.rpt_mode = cwiid.RPT_BTN
