import threading
import io
import socket
import struct
import time
from time import sleep
from threading import Thread

# Set server IP address & Port
HOST = "10.217.202.76"
PORT = 8001
BUFFER_SIZE = 1024
        
# give command to car
def drive():
    drive_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # drive_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    drive_socket.connect((HOST, PORT))  #Bind to the port

    print('server ready to receive command')
    try:
        while True:
            # Read command received from server
            cmd = drive_socket.recv(BUFFER_SIZE)
            print(cmd)
            # if (cmd == 1): # drive forward
                # print("Forward")
            # elif (cmd == 2): # drive left
                # print("Left");
            # elif (cmd == 3): # drive right
                # print("Right");
            # elif (cmd == 12): # drive forward and right
                # print("Forward Right");
            # elif (cmd == 13): # drive forward and left
                # print("Right");
            # elif (cmd == -1):
                # print("Reverse")
            # elif (cmd == 0): # stop
                # print("Stop");          
    except:
        print("ERROR (drive_server.drive) -> Error occured")
    finally:
        drive_socket.close()
        

Thread(target = drive).start()

