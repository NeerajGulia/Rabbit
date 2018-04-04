import camera_stream
import drive_client
from threading import Thread

#Start threads
Thread(target = camera_stream.streamCamera).start()
#Start threads
Thread(target = drive_client.driveCommand).start()