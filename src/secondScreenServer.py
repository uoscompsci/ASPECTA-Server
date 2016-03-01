import socket
import select
import sys
import time
import ujson as json
import base64
from threading import Thread
from API import apiMessageParser
from collections import deque
from ConfigParser import SafeConfigParser

queue = deque([])
sock2usr = {}
app2sock = {}
sock2app = {}
loop = True

#Constantly monitors the queue for received messages
def message_queue_monitor():
	counter = 0
	while(loop):
		time.sleep(0.001)
		while(len(queue)!=0):
			qitem = queue.pop()
			appsplit = sock2app[qitem[0]].split(',')
			temp = qitem[1]
			temp['IDuser'] = sock2usr[qitem[0]]
			temp['IDapp'] = appsplit[0]
			temp['IDinstance'] = appsplit[1]
			if(temp['call'] == "set_rectangle_texture" or temp['call'] == "new_texrectangle" or temp['call'] == "new_texrectangle_with_ID"):
				g = open("images/" + str(counter) + "." + str(temp['extension']), "w")
				g.write(base64.decodestring(str(temp['textureData'])))
				g.close()
				temp['imageID'] = counter
				counter += 1
			#qitem = (qitem[0], json.dumps(temp))
			reply(qitem[0],messageParser.processMessage(temp))
#Sends a reply to the client that the last message was received from 
def reply (sock, message):
	for socket in CONNECTION_LIST:
		if socket == sock :
			try :
				jsonmessage = json.dumps(message)
				socket.send(jsonmessage)
			except :
				socket.close()
				CONNECTION_LIST.remove(socket)
 
if __name__ == "__main__":
	
	parser = SafeConfigParser()
	parser.read("secondScreenConfig.ini")
	RECV_BUFFER = parser.getint('connection','RecieveBuffer')
	PORT = parser.getint('connection','port')
	HOST = parser.get('connection','host')
	 
	CONNECTION_LIST = []
	 
	server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	server_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
	server_socket.bind((HOST, PORT))
	server_socket.listen(10)
 
	CONNECTION_LIST.append(server_socket)
	
	print "API server started on port " + str(PORT)
	
	messageParser = apiMessageParser() #Create a parser for API messages which are received
	
	#Create and start a thread which will monitor the queue of received API messages
	queueMonitor = Thread(target = message_queue_monitor)
	queueMonitor.start()
	
	loop = True
	
	#Loop until the looping flag changes
	while(loop):
		time.sleep(0.001)
		try:
			read_sockets = select.select(CONNECTION_LIST,[],[])[0] #Wait until ready for IO
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
					recieved = int(sock.recv(10))
					data = ""
					while (recieved>0):
						temp = sock.recv(RECV_BUFFER)
						data += temp
						recieved -= len(temp)
					dataJSON = json.loads(data)
					if data:
						if(dataJSON['call'] == 'quit'): #If the received data is a quit command close the socket and exit
							print '\033[1;31mShutting down server\033[1;m'
							messageParser.processMessage(data)
							loop=False
						elif(dataJSON['call'] == 'login'):
							if(sock2usr.has_key(sock)==False):
								sock2usr[sock] = dataJSON['username']
								reply(sock,str({}))
							else:
								reply(sock,str({'error' : 4}))
						elif(dataJSON['call'] == 'setapp'):
							if(sock2app.has_key(sock)):
								reply(sock,str({'error' : 5}))
							else:
								count = 0
								added = False
								while(added==False):
									if(app2sock.has_key(dataJSON['appname'] + "," + str(count))==False):
										app2sock[dataJSON['appname'] + "," + str(count)] = sock
										sock2app[sock] = dataJSON['appname'] + "," + str(count)
										reply(sock,str({}))
										added = True
									else:
										count += 1
						else: #If the message isn't a quit command puts the received API message onto the queue to be processed
							if(sock2usr.has_key(sock) and sock2app.has_key(sock)):
							 	queue.appendleft((sock,dataJSON))
							else:
								if(sock2usr.has_key(sock)==False):
									reply(sock,str({'error' : 3}))
								else:
									reply(sock,str({'error' : 6}))
				except:
					print "Client (%s, %s) is offline" % addr
					sock.close()
					CONNECTION_LIST.remove(sock)
					continue
	server_socket.close()
	time.sleep(0.2)
	sys.exit(0)