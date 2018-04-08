#!/usr/bin/python3
import RPi.GPIO as IO
import time

class RPI_:

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
        except Exception as e:
            print ("ErrorOccured -> RPI_.forward -> ",e)
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
        except Exception as e:
            print ("ErrorOccured -> RPI_.backward -> " ,e)
            self.reset()

    def left(self): 
        try:
            IO.output(self.steer_pin_4,IO.LOW)
            IO.output(self.steer_pin_3,IO.HIGH) 
            if self.withTimeSleep == True:
                time.sleep(self.timeinMs)
                self.reset()
        except Exception as e :
            print ("ErrorOccured -> RPI_.left -> ",e)
            self.reset()

    def right(self):
        try:
            IO.output(self.steer_pin_4,IO.HIGH)
            IO.output(self.steer_pin_3,IO.LOW)
            if self.withTimeSleep == True:
                time.sleep(self.timeinMs)
                self.reset()
        except Exception as e:
            print ("ErrorOccured -> RPI_.right -> ",e)
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
        except Exception as e:
            print ("ErrorOccured -> RPI_.forwardLeft -> ",e)
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
        except Exception as e:
            print ("ErrorOccured -> RPI_.forwardRight ->" ,e )
            self.reset()

       def backwardLeft(self):
        try:
            IO.output(self.motor_pin_4,IO.LOW)
            IO.output(self.motor_pin_2,IO.LOW)
            IO.output(self.motor_pin_1,IO.HIGH)
            IO.output(self.motor_pin_3,IO.HIGH)
            IO.output(self.steer_pin_4,IO.LOW)
            IO.output(self.steer_pin_3,IO.HIGH)
            if self.withTimeSleep == True:
                time.sleep(self.timeinMs)
                self.reset()
        except Exception as e:
            print ("ErrorOccured -> RPI_.backwardLeft -> " ,e )
            self.reset()

    def backwardRight(self):
        try:
            IO.output(self.motor_pin_4,IO.LOW)
            IO.output(self.motor_pin_2,IO.LOW)
            IO.output(self.motor_pin_1,IO.HIGH)
            IO.output(self.motor_pin_3,IO.HIGH)
            IO.output(self.steer_pin_4,IO.HIGH)
            IO.output(self.steer_pin_3,IO.LOW)
            if self.withTimeSleep == True:
                time.sleep(self.timeinMs)
                self.reset()
        except Exception as e:
            print ("ErrorOccured -> RPI_.backwardRight -> " ,e )
            self.reset()        
    
    def reset(self):
        try:
            IO.output(self.motor_pin_1,IO.LOW)
            IO.output(self.motor_pin_2,IO.LOW)
            IO.output(self.motor_pin_3,IO.LOW)
            IO.output(self.motor_pin_4,IO.LOW)
            IO.output(self.steer_pin_3,IO.LOW)
            IO.output(self.steer_pin_4,IO.LOW)

        except Exception as e:
            print ("ErrorOccured -> RPI_.reset -> ",e)
            IO.cleanup()