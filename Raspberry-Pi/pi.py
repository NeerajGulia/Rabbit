import camera_server
import drive_client
from threading import Thread

#Start threads
Thread(target = camera_server.VideoStream).start()
#Start threads
Thread(target = drive_client.drive).start()