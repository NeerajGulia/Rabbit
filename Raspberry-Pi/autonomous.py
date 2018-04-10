import numpy as np
import socket
import time
import struct
import sys
sys.path.insert(0, '../lib')
from utils import *
import curses
from curses import wrapper
import logging

class Autonomous(object):
    
    def __init__(self):
        self.screen = None
        curses.noecho()     
        curses.cbreak()
        nodelay(True)
        print('Ready for Autonomous...')
        self.video_socket, self.video_connection, self.drive_socket, self.drive_client = getConnections()
        print('connection created...')
        self.send_inst = True
        logging.basicConfig(filename='automous.log',level=logging.DEBUG)
        curses.wrapper(self.processImage)
        # self.processImage()  

    def sendCommand2Car(self, manualCommand, predictedCommand):
        if (manualCommand is None):
            printText('Predicted Command: ', predictedCommand)
            self.drive_client.sendall(str.encode(predictedCommand))
        else:
            printText('Predicted Command: {}, manualCommand: {}'.format(predictedCommand, manualCommand))
            self.drive_client.sendall(str.encode(manualCommand))
    
    def processImage(self, stdscr):
        self.screen = stdscr
        self.screen.clear()
        # stream video frames one by one
        try:
            while self.send_inst:
                image = getImage(self.video_connection)
                key = self.screen.getch()
                printText('key pressed: {}'.format(key), 10, 10)
                #send image to model to get the drive command
                predictedCommand = Movement.RIGHT #Predicted Image
                # self.send_inst, isAutonomous = processInput(self.sendCommand2Car, predictedCommand)
                # if (isAutonomous):
                self.send_inst, isAutonomous = mapCursor2Movement(self.sendCommand2Car, key, predictedCommand)
                # Clear the terminal
        except Exception as e:
            error = 'ERROR -> Autonomous.processImage: {}'.format(e)
            print(error)
            logging.error(error)
        finally:
            self.drive_client.sendall(str.encode(QUIT_RC))
            self.video_connection.close()
            self.video_socket.close()
            self.drive_client.close()
            self.drive_socket.close()

    def printText(self,  message, y = 0, x = 0):
        self.screen.addstr(y, x, message)
        self.screen.refresh()
        
if __name__ == '__main__':
    Autonomous()
