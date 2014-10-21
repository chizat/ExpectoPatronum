#!/usr/bin/python
import cwiid
import time

# Connect to the Wii Remote. 

class Wiimote:

	wiimote = ""
	
	def connect(self):
		try:
			time.sleep(1)
			self.wiimote = cwiid.Wiimote()
		except RuntimeError:
			self.connect()
	
	def connect_wiimote(self):
		self.connect()

		self.wiimote.led = 6
		self.wiimote.rpt_mode = cwiid.RPT_BTN

	def validate_connection(self):
		try:
			self.wiimote.request_status()
		except RuntimeError:
			self.wiimote = self.connect_wiimote()
		time.sleep(1)

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
