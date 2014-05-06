import socket
import select
import sys
from threading import Thread
from Queue import Queue
from API import apiMessageParser

queue = Queue([999])
usr2sock = {}
sock2usr = {}

#Constantly monitors the queue for received messages
def message_queue_monitor():
	while(True):
		if(queue.empty()!=True):
			qitem = queue.get()
			reply(qitem[0],str(messageParser.processMessage(qitem[1] + "," + sock2usr[qitem[0]])))

#Sends a reply to the client that the last message was received from 
def reply (sock, message):
	for socket in CONNECTION_LIST:
		if socket == sock :
			try :
				socket.send(message)
			except :
				socket.close()
				CONNECTION_LIST.remove(socket)
 
if __name__ == "__main__":
	 
	CONNECTION_LIST = []
	RECV_BUFFER = 4096
	PORT = 5000
	 
	server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # why is this not working?
	server_socket.bind(("0.0.0.0", PORT))
	server_socket.listen(10)
 
	CONNECTION_LIST.append(server_socket)
	
	print "API server started on port " + str(PORT)
	
	messageParser = apiMessageParser() #Create a parser for API messages which are received
	
	#Create and start a thread which will monitor the queue of received API messages
	queueMonitor = Thread(target = message_queue_monitor)
	queueMonitor.start()
	
	loop = True
	
	#Loop until the looping flag changes
	while(loop==True):
		try:
			read_sockets,write_sockets,error_sockets = select.select(CONNECTION_LIST,[],[]) #Wait until ready for IO
		except:
	   		continue #Start loop again
 
 		#Loop through all the read sockets
		for sock in read_sockets:
			if sock == server_socket: #If a new client is connecting add it to the connection list
				sockfd, addr = server_socket.accept()
				CONNECTION_LIST.append(sockfd)
				print "Client (%s, %s) connected" % addr
			else:
				try: #Try to receive data and process it
					data = sock.recv(RECV_BUFFER)
					if data:
						if(data == "quit"): #If the received data is a quit command close the socket and exit
							print '\033[1;31mShutting down server\033[1;m'
							loop=False
						elif(data.startswith("login,")):
							pieces = data.split(',')
							if(usr2sock.has_key(pieces[1])==False):
								if(sock2usr.has_key(sock)==False):
									usr2sock[pieces[1]] = sock
									sock2usr[sock] = pieces[1]
								else:
									reply(sock,str({'error' : 5}))
							else:
								reply(sock,str({'error' : 4}))
						else: #If the message isn't a quit command puts the received API message onto the queue to be processed
							if(sock2usr.has_key(sock)):
							 	queue.put((sock,data))
							else:
				 				reply(sock,str({'error' : 3}))
				except:
					print "Client (%s, %s) is offline" % addr
					sock.close()
					CONNECTION_LIST.remove(sock)
					continue
	server_socket.close()