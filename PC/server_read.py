import io
import socket
import struct
from PIL import Image
import numpy as np
from threading import Thread
import random

# Set server IP address & Port
HOST = "0.0.0.0" # all interfaces
VIDEO_PORT = 8000
DRIVE_PORT = 8001
IMAGE_SIZE = 320 * 240 * 3 # 320x240 resolution with 3 channel image

# Load a frame from the client Raspberry Pi to process
def get_image(video_socket):

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
    stream_image = Image.open(image_stream)
    # Convert image to numpy array
    stream_image = np.array(stream_image)

    # Check to see if full image has been loaded - this prevents errors due to images lost over network
    if stream_image.size != IMAGE_SIZE:
        print("ERROR (get_image) -> unexpected image size: expected: {}, got: {}".format(IMAGE_SIZE, stream_image.size))
        return 0

    return stream_image 
    
def autonomous():

    # Set up drive server and wait for a connect
    print("Waiting for drive Client")
    drive_socket = socket.socket()  # Create a socket object
    drive_socket.bind((HOST, DRIVE_PORT))  # Bind to the port

    drive_socket.listen(0)  # Wait for client connection
    # Wait for client to connect
    drive_client, _ = drive_socket.accept()

    print("Command client connected!")
    
    # Start a socket listening for connections on 0.0.0.0:8000 (0.0.0.0 means
    # all interfaces)
    # video_socket = socket.socket()
    # video_socket.bind((HOST, VIDEO_PORT))
    # video_socket.listen(0)

    # # Accept a single connection and make a file-like object out of it
    # video_connection = video_socket.accept()[0].makefile('rb')
    try:
        while True:
            # Read the length of the image as a 32-bit unsigned int. If the
            # length is zero, quit the loop
            # image = get_image(video_connection)
            # if (len(image) == 0)
                # print("ERROR (server_read.autonomous)-> image length is 0, exiting")
                # break
            #get value from NN get_direction(image)
            # pass the direction to pi to steer the car
            value = random.randint(0, 10)
            drive_client.send(str(value)) # 1 is forward
            print('sent {} to client'.format(value))
    finally:
        # video_connection.close()
        drive_client.close()
        drive_socket.close()
        # video_socket.close()
        
# Start thread (Thread 1)
Thread(target=autonomous).start()
