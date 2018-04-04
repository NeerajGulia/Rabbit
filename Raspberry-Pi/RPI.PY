#!/usr/bin/python3
import RPi.GPIO as IO
import time

class RPI_:

	#motor_pin_1
	#motor_pin_2
	#motor_pin_3=None
	#motor_pin_4=None
	#steer_pin_3=None
	#steer_pin_4=None
	#timestep=None
	#timeinMs=0
	#withTimeSleep = True
	
	def init_motorpin(self):
		IO.setwarnings(False)
		IO.setmode(IO.BOARD)
		self.motor_pin_1=35
		self.motor_pin_2=36
		self.motor_pin_3=37
		self.motor_pin_4=38
		self.steer_pin_3=31
		self.steer_pin_4=32
		IO.setup(self.motor_pin_1,IO.OUT)
		IO.setup(self.motor_pin_2,IO.OUT)
		IO.setup(self.motor_pin_3,IO.OUT)
		IO.setup(self.motor_pin_4,IO.OUT)
		IO.setup(self.steer_pin_3,IO.OUT)
		IO.setup(self.steer_pin_4,IO.OUT)

		
	def __init__(self,time_=250,timeFlag=True):
		self.timestep=time_
		self.withTimeSleep= timeFlag
		self.timeinMs = self.timestep/1000.0		
		self.init_motorpin()
		
	def forward(self):
		try:
			IO.output(self.motor_pin_1,IO.LOW)
			IO.output(self.motor_pin_3,IO.LOW)
			IO.output(self.motor_pin_4,IO.HIGH)
			IO.output(self.motor_pin_2,IO.HIGH)
			if self.withTimeSleep == True:
				time.sleep(self.timeinMs)		
				self.reset()
		except:
			print ("Exception in forward function")
			self.reset()
			
	def backward(self):
	
		try:
			IO.output(self.motor_pin_4,IO.LOW)
			IO.output(self.motor_pin_2,IO.LOW)
			IO.output(self.motor_pin_1,IO.HIGH)
			IO.output(self.motor_pin_3,IO.HIGH)
			if self.withTimeSleep == True:
				time.sleep(self.timeinMs)
				self.reset()
		except:
			print ("Exception in backward function")
			self.reset()

	def forwardLeft(self):
	
		try:
			IO.output(self.motor_pin_1,IO.LOW)
			IO.output(self.motor_pin_3,IO.LOW)
			IO.output(self.motor_pin_4,IO.HIGH)
			IO.output(self.motor_pin_2,IO.HIGH)
			IO.output(self.steer_pin_4,IO.LOW)
			IO.output(self.steer_pin_3,IO.HIGH)
			if self.withTimeSleep == True:
				time.sleep(self.timeinMs)
				self.reset()
		except:
			print ("Exception in forwardLeft function")
			self.reset()

	def forwardRight(self):
	
		try:
			IO.output(self.motor_pin_1,IO.LOW)
			IO.output(self.motor_pin_3,IO.LOW)
			IO.output(self.motor_pin_4,IO.HIGH)
			IO.output(self.motor_pin_2,IO.HIGH)
			
			IO.output(self.steer_pin_4,IO.HIGH)
			IO.output(self.steer_pin_3,IO.LOW)
			if self.withTimeSleep == True:
				time.sleep(self.timeinMs)
				self.reset()
		except:
			print ("Exception in forwardRight function")
			self.reset()

       
	def left(self): 
	
		try:
			IO.output(self.steer_pin_4,IO.LOW)
			IO.output(self.steer_pin_3,IO.HIGH)	
			if self.withTimeSleep == True:
				time.sleep(self.timeinMs)
				self.reset()
		except:
			print ("Exception in left function")
			self.reset()

	def right(self):
	
		try:
			IO.output(self.steer_pin_4,IO.HIGH)
			IO.output(self.steer_pin_3,IO.LOW)
			if self.withTimeSleep == True:
				time.sleep(self.timeinMs)
				self.reset()
		except:
			print ("Exception in right function")
			self.reset()

    
	def reset(self):
	
		try:
			IO.output(self.motor_pin_1,IO.LOW)
			IO.output(self.motor_pin_2,IO.LOW)
			IO.output(self.motor_pin_3,IO.LOW)
			IO.output(self.motor_pin_4,IO.LOW)
			IO.output(self.steer_pin_3,IO.LOW)
			IO.output(self.steer_pin_4,IO.LOW)

		except:
			print ("Exception in reset function")
			IO.cleanup()
