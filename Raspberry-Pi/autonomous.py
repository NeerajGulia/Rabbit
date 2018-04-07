import numpy as np
import socket
import time
import struct
import sys
sys.path.insert(0, '../lib')
from utils import *

class Autonomous(object):
    
    def __init__(self):
        self.video_socket, self.video_connection, self.drive_socket, self.drive_client = getConnections()
        
        self.send_inst = True
        self.processImage()
    
    def sendCommand2Car(self, command):
        print('command predicted: ', command)
        self.drive_client.send(str.encode(command))
    
    def processImage(self):
        # stream video frames one by one
        try:
            while self.send_inst:
                image = getImage(self.video_connection)
                #send image to model to get the drive command
                command = Movement.RIGHT #predictCommand(image)
                self.sendCommand2Car(command)
        except Exception as e:
                print('ERROR -> Autonomous.processImage: ', e)
        finally:
            self.drive_client.send(str.encode(STOP_RC))        
            self.video_connection.close()
            self.video_socket.close()
            self.drive_client.close()
            self.drive_socket.close()

if __name__ == '__main__':
    Autonomous()
