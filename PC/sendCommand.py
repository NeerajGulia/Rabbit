import io
import numpy as np
import cv2
import pygame
from pygame.locals import *
import socket
import time
import os
import struct
import sys
from PIL import Image


# Set server IP address & Port
HOST = "0.0.0.0" #empty means it will listen on all ip address locally
VIDEO_PORT = 8000
IMAGE_SIZE = 320 * 240 * 3

DRIVE_PORT = 8001

class Movement():
    UP         = "W"
    DOWN       = "S"
    LEFT       = "A"
    RIGHT      = "D"
    UP_RIGHT   = "[W,D]"
    UP_LEFT    = "[A,W]"
    DOWN_LEFT  = "[A,S]"
    DOWN_RIGHT = "[S,D]"
        

class CollectTrainingData(object):
    
    def __init__(self):
        self.send_inst = True
        # drive socket and connection
        self.drive_socket = socket.socket()
        self.drive_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.drive_socket.bind((HOST, DRIVE_PORT))
        self.drive_socket.listen(0)
        
        self.drive_client, _ = self.drive_socket.accept()
        
        pygame.init()
        pygame.key.set_repeat(1,50) #1 is delay and 50 is interval in ms
        self.screen = pygame.display.set_mode((320, 240))
        self.collect_image()

    def appendCommand(self, command, fileName, image):
        print('command pressed: ', command)
        self.drive_client.send(str.encode(command))
    
    def collect_image(self):
        
        try:
            frameCount = 1
            while self.send_inst:
                image = None
                fileName = "hi"
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        print('Exiting now')
                        self.send_inst = False
                        break;
                    
                    elif event.type == KEYDOWN:
                        key_input = pygame.key.get_pressed()
                        if key_input[pygame.K_UP] and key_input[pygame.K_RIGHT]:
                            self.appendCommand(Movement.UP_RIGHT, fileName, image)
                            #give control to RC to move forward right
            
                        elif key_input[pygame.K_UP] and key_input[pygame.K_LEFT]:
                            self.appendCommand(Movement.UP_LEFT, fileName, image)
                            
                        # simple orders
                        elif key_input[pygame.K_UP]:
                            self.appendCommand(Movement.UP, fileName, image)
                            
                        elif key_input[pygame.K_DOWN]:
                            self.appendCommand(Movement.DOWN, fileName, image)
                            
                        elif key_input[pygame.K_RIGHT]:
                           self.appendCommand(Movement.RIGHT, fileName, image)
                            
                        elif key_input[pygame.K_LEFT]:
                            self.appendCommand(Movement.LEFT, fileName, image)
                            
                        elif key_input[pygame.K_x] or key_input[pygame.K_q]:
                            print('exit')
                            self.send_inst = False
                            self.drive_client.send(str.encode('X'))
                            break
                    
            print('Done')

        finally:
            self.drive_client.close()
            self.drive_socket.close()
            pygame.quit()

if __name__ == '__main__':
    CollectTrainingData()
