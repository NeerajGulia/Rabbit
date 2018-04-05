import io
import socket
import struct
import time
import picamera
import constants

def streamCamera():
    print('Stream camera start...')
    # Set server IP address & Port
        
    video_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    video_socket.connect((constants.HOST, constants.VIDEO_PORT))
    video_connection = video_socket.makefile('wb')
    print('video connection successfull...')
    try:
        with picamera.PiCamera() as camera:
            camera.resolution = constants.CAMERA_RESOLUTION      # pi camera resolution
            camera.framerate = constants.FRAMERATE               # 10 frames/sec
            #camera.rotation = 90
            camera.vflip = True #flip the image upside down since the camera is placed upside down
            camera.hflip = True #flip the image from left to right, to correct the upside down. Else right will appear left and vice versa
            time.sleep(2)                       # give 2 secs for camera to initilize
            start = time.time()
            stream = io.BytesIO()
            
            # send jpeg format video stream
            for foo in camera.capture_continuous(stream, 'jpeg', use_video_port = True):
                video_connection.write(struct.pack('<L', stream.tell()))
                # print("data size: {0}".format(stream.tell()))
                video_connection.flush()
                stream.seek(0)
                video_connection.write(stream.read())
                stream.seek(0)
                #print("sending data 3")
                stream.truncate()
                #print("sending data 4")
        video_connection.write(struct.pack('<L', 0))
    except Exception as e:
        print("ERROR (camera_stream.streamCamera) -> ", e)
    finally:
        print('Stream camera end')
        video_connection.close()
        video_socket.close()

