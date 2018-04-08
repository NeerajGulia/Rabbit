import io
import socket
import RPI
import constants
        
# give command to car
def driveCommand():
    rcControl = RPI.RPI_()
    print('drive command start...')
    # Set server IP address & Port
    drive_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    drive_socket.connect((constants.HOST, constants.DRIVE_PORT))  #Bind to the port

    print('drive connection successfull...')
    try:
        while True:
            # Read command received from server
            cmd = drive_socket.recv(constants.BUFFER_SIZE)
            command = cmd.decode().lower().strip()
            print("received: ", command)
            
            if (command == "x" or len(command) == 0): # drive forward
                print('Exiting drive')
                rcControl.reset()
                break
            elif(command == 'a'): 
                rcControl.left()
            elif(command == 'd'):
                rcControl.right()
            elif(command == 'w'):   
                rcControl.forward()                
            elif(command == 's'):
                rcControl.backward()
            elif(command == '[a,w]' or command == '[w,a]'):
                rcControl.forwardLeft()
            elif(command == '[w,d]' or command == '[d,w]'):
                rcControl.forwardRight()
            elif(command == '[a,s]' or command == '[s,a]'):
                rcControl.backwardLeft()
            elif(command == '[s,d]' or command == '[d,s]'):
                rcControl.backwardRight()   
            else:
                rcControl.reset()       
    except Exception as e:
        print("ERROR (drive_server.driveCommand) -> Error occured: ", e)
    finally:
        print('drive command end...')
        drive_socket.close()