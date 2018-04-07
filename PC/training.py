import numpy as np
import cv2
import pygame
from pygame.locals import *
import socket
import time
import struct
import sys
sys.path.insert(0, '../lib')
from utils import *

class CollectTrainingData(object):
    
    def __init__(self):
        self.video_socket, self.video_connection, self.drive_socket, self.drive_client = getConnections()
        
        self.send_inst = True
        self.savedFrameCount = 0
        self.fileNames = []
        self.commands = []

        pygame.init()
        pygame.key.set_repeat(1,50) #1 is delay and 50 is interval in ms. Without this the continuous key press wont be registered
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.collect_image()
    
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
                image = getImage(self.video_connection)
                # save streamed images
                fileName = 'training_images/frameCount{:>05}.jpg'.format(frameCount)
                self.screen.blit(pygame.surfarray.make_surface(image),(0,0))
                pygame.display.update() #update the display with new image
                cv2.imshow('image', image)
                frameCount += 1
                self.send_inst = processInput(self.appendCommand, fileName, image)

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
