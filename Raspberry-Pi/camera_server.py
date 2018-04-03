import threading
import io
import socket
import struct
import time
import picamera
import serial
from time import sleep

# Set server IP address & Port
HOST = "192.168.0.100"
PORT = 8000
CAMERA_RESOLUTION = (320,240)
FRAMERATE = 10
        
# Thread to handle video transmission
def stream():
    print("Connecting to video server")
    video_socket = socket.socket()
    video_socket.connect((HOST, PORT))

    # Make a file-like object out of the connection
    connection = video_socket.makefile('wb')
    print("Should be connected to video server")
    try:
        camera = picamera.PiCamera()
        camera.resolution = CAMERA_RESOLUTION
        camera.framerate = FRAMERATE
        # Start a preview and let the camera warm up for 2 seconds
        # camera.start_preview()
        time.sleep(2)

        # Note the start time and construct a stream to hold image data
        # temporarily (we could write it directly to connection but in this
        # case we want to find out the size of each capture first to keep
        # our protocol simple)
        start = time.time()
        stream = io.BytesIO()
        for foo in camera.capture_continuous(stream, 'jpeg',use_video_port = True):
            # Write the length of the capture to the stream and flush to
            # ensure it actually gets sent
            connection.write(struct.pack('<L', stream.tell()))
            connection.flush()
            # Rewind the stream and send the image data over the wire
            stream.seek(0)
            connection.write(stream.read())
            # If we've been capturing for more than 30 seconds, quit
            if time.time() - start > 30:
               print("WARNING -> capturing more than 30 seconds..");
            # Reset the stream for the next capture
            stream.seek(0)
            stream.truncate()
        # Write a length of zero to the stream to signal we're done
        connection.write(struct.pack('<L', 0))
    except:
        print("ERROR (camera_client.stream) -> Exception occured")
    finally:        
        video_socket.close()    
        connection.close()
