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
VIDEO_HOST = "0.0.0.0" #empty means it will listen on all ip address locally
VIDEO_PORT = 8000
IMAGE_SIZE = 320 * 240 * 3

DRIVE_HOST = "0.0.0.0"
DRIVE_PORT = 8001
STOP_RC = ' x  '

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
        # video socket and connection
        self.video_socket = socket.socket()
        self.video_socket.bind((VIDEO_HOST, VIDEO_PORT))
        self.video_socket.listen(0)
        # accept a single connection
        self.video_connection = self.video_socket.accept()[0].makefile('rb')

        # drive socket and connection
        self.drive_socket = socket.socket()
        self.drive_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.drive_socket.bind((DRIVE_HOST, DRIVE_PORT))
        self.drive_socket.listen(0)
        
        self.drive_client, _ = self.drive_socket.accept()
        
        #connect to a seral port
        self.send_inst = True
        self.savedFrameCount = 0
        self.fileNames = []
        self.commands = []

        pygame.init()
        pygame.key.set_repeat(1,50) #1 is delay and 50 is interval in ms
        self.screen = pygame.display.set_mode((320, 240))
        self.collect_image()

    # Load a frameCount from the client Raspberry Pi to process
    def get_image(self, video_socket):

        image_len = struct.unpack('<L', video_socket.read(struct.calcsize('<L')))[0]
        if not image_len:
            print("Break as image length is null")
            return 0
        # Construct a stream to hold the image data and read the image
        # data from the connection
        image_stream = io.BytesIO()
        image_stream.write(video_socket.read(image_len))
        # Rewind the stream, open it as an image with PIL
        image_stream.seek(0)
        image = Image.open(image_stream)
        # Convert image to numpy array
        img_array = np.array(image)

        # Check to see if full image has been loaded - this prevents errors due to images lost over network
        if img_array.size != IMAGE_SIZE:
            print("ERROR (get_image) -> unexpected image size: expected: {}, got: {}".format(IMAGE_SIZE, img_array.size))
            return 0

        return img_array 
    
    def appendCommand(self, command, fileName, image):
        print('command pressed: ', command)
        self.savedFrameCount += 1
        self.commands.append(command)
        self.fileNames.append(fileName)
        cv2.imwrite(fileName, image)
        self.drive_client.send(str.encode(command))
    
    def collect_image(self):
        saved_frame = 0

        # collect images for training
        print('Start collecting images...')
        e1 = cv2.getTickCount()
        
        # stream video frames one by one
        try:
            frameCount = 1
            while self.send_inst:
                frameSaved = False;
                img_array = self.get_image(self.video_connection)
                # print("len: {}, shape: {}".format(len(img_array), img_array.shape))
                image = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
                # select lower half of the image
                # roi = image[120:240, :]
                
                # save streamed images
                fileName = 'training_images/frameCount{:>05}.jpg'.format(frameCount)
                self.screen.blit(pygame.surfarray.make_surface(image),(0,0))
                pygame.display.flip()
                # print(fileName)
                # cv2.imshow('image', image)
                frameCount += 1
            
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
                            break
            # signal to drive_client to stop receiving the messages
            self.drive_client.sendall(str.encode(STOP_RC))        
            try:    
                np.savetxt('training_data.csv', (list(zip(self.fileNames, self.commands))), delimiter=',', fmt="%s")
            except IOError as e:
                print(e)

            e2 = cv2.getTickCount()
            # calculate streaming duration
            time0 = (e2 - e1) / cv2.getTickFrequency()

            print('Streaming duration:', time0)
            print('Total frameCount:', frameCount)
            print('Saved frameCount:', self.savedFrameCount)
            print('Dropped frameCount', frameCount - self.savedFrameCount)
        except Exception as e:
                print('ERROR -> training.collect_image: ', e)
        finally:
            self.drive_client.send(str.encode(STOP_RC))        
            self.video_connection.close()
            self.video_socket.close()
            self.drive_client.close()
            self.drive_socket.close()
            pygame.quit()

if __name__ == '__main__':
    CollectTrainingData()
