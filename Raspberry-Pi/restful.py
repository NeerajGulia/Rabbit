from flask import Flask
from flask import jsonify
app = Flask(__name__)
import RPI

@app.route("/")
def test():
    return "API is working fine"
	
r= RPI.RPI_()
# endpoint to give command
@app.route("/give_command/<command>", methods=["GET"])
def push_command(command):
  	#RPI.reset()	
	command = command.lower()
	if(command=='l'): 
		try:
			print ("running left command")	
			r.left()
		except:
			print ("error in command " , command)	
	elif(command == 'r'):
		try:
			r.right()
		except:
			 print ("error in command " , command)
	elif(command == 'u'):	
		r.forward()
		
	elif(command == 'd'):
		r.backward()
		
	elif(command == 'l,u' or command == 'u,l'):
		r.forwardLeft()
	
	elif(command == 'r,u' or command == 'u,r'):
		r.forwardRight()
	
	else:
		r.reset()

	return "true"
if __name__ == '__main__':
    app.run(host='192.168.43.240',port=5000,debug=True)
