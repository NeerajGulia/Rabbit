import cv2
import struct
import socket
import pygame
from pygame.locals import *
import numpy as np

VIDEO_HOST = "0.0.0.0" #empty means it will listen on all ip address locally
VIDEO_PORT = 8000
WIDTH = 320
HEIGHT = 240
IMAGE_SIZE = WIDTH * HEIGHT * 3

DRIVE_HOST = "0.0.0.0"
DRIVE_PORT = 8001
STOP_RC = 'x'
QUIT_RC = '~'

class Movement():
    UP         = "W"
    DOWN       = "S"
    LEFT       = "A"
    RIGHT      = "D"
    UP_RIGHT   = "[W,D]"
    UP_LEFT    = "[A,W]"
    DOWN_LEFT  = "[A,S]"
    DOWN_RIGHT = "[S,D]"

# Load a frameCount from the client Raspberry Pi to process
def getImage(video_connection):
    image_len = struct.unpack('<L', video_connection.read(struct.calcsize('<L')))[0]
    if not image_len:
        print("Break as image length is null")
        return 0
    file_bytes = np.asarray(bytearray(video_connection.read(image_len)), dtype=np.uint8)
    return cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

def getConnections():
    # video socket and connection
    video_socket = socket.socket()
    video_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    video_socket.bind((VIDEO_HOST, VIDEO_PORT))
    video_socket.listen(0)
    # accept a single connection
    video_connection = video_socket.accept()[0].makefile('rb')

    # drive socket and connection
    drive_socket = socket.socket()
    drive_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    drive_socket.bind((DRIVE_HOST, DRIVE_PORT))
    drive_socket.listen(0)
    
    drive_client, _ = drive_socket.accept()
    return video_socket, video_connection, drive_socket, drive_client

def processInput(executeCommand, *argv):
    send_inst = True
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print('Exiting now')
            send_inst = False
            break;
        
        elif event.type == KEYDOWN:
            key_input = pygame.key.get_pressed()

            #dual commands
            if (key_input[pygame.K_UP] and key_input[pygame.K_RIGHT]) or key_input[pygame.K_e]:
                executeCommand(Movement.UP_RIGHT, *argv)
            elif (key_input[pygame.K_UP] and key_input[pygame.K_LEFT]) or key_input[pygame.K_q]:
                executeCommand(Movement.UP_LEFT, *argv)
            elif (key_input[pygame.K_DOWN] and key_input[pygame.K_RIGHT]) or key_input[pygame.K_c]:
                executeCommand(Movement.DOWN_RIGHT, *argv)
            elif (key_input[pygame.K_DOWN] and key_input[pygame.K_LEFT]) or key_input[pygame.K_z]:
                executeCommand(Movement.DOWN_LEFT, *argv)
            
            #single commands
            elif key_input[pygame.K_UP] or key_input[pygame.K_w]:
                executeCommand(Movement.UP, *argv)
            elif key_input[pygame.K_DOWN] or key_input[pygame.K_s]:
                executeCommand(Movement.DOWN, *argv)
            elif key_input[pygame.K_RIGHT] or key_input[pygame.K_d]:
                executeCommand(Movement.RIGHT, *argv)
            elif key_input[pygame.K_LEFT] or key_input[pygame.K_a]:
                executeCommand(Movement.LEFT, *argv)
            elif key_input[pygame.K_x]:
                print('exit')
                send_inst = False
                break
    return send_inst

def mapCursor2Movement(executeCommand, key, *argv):
    send_inst = True
    isAutonomous = True
    if (key == ord('e')):
        executeCommand(Movement.UP_RIGHT, *argv)
        isAutonomous = False
    elif (key == ord('q')):
        executeCommand(Movement.UP_LEFT, *argv)
        isAutonomous = False
    elif (key == ord('c')):
        executeCommand(Movement.DOWN_RIGHT, *argv)
        isAutonomous = False
    elif (key == ord('z')):
        isAutonomous = False
        executeCommand(Movement.DOWN_LEFT, *argv)
    
    elif (key == ord('w')):
        executeCommand(Movement.UP, *argv)
        isAutonomous = False
    elif (key == ord('s')):
        executeCommand(Movement.DOWN, *argv)
        isAutonomous = False
    elif (key == ord('d')):
        executeCommand(Movement.RIGHT, *argv)
        isAutonomous = False
    elif (key == ord('a')):
        executeCommand(Movement.LEFT, *argv)
        isAutonomous = False
    elif (key == ord('x')):
        print('exit')
        send_inst = False
    else:
        executeCommand(None, *argv)
        
    return send_inst, isAutonomous
