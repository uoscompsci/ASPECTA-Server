import socket
import sys
import time
from threading import Thread
from API import apiMessageParser

queue = []

#Continually scans the queue for tasks, and if there are any present processes them in order
def message_queue_monitor():
	while(True):
		if(len(queue)>0):
			qitem = queue.pop(0)
			messageParser.processMessage(qitem)

ANY = '0.0.0.0'
MCAST_ADDR = '224.168.2.9'
MCAST_PORT = 1602
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
sock.bind((ANY,MCAST_PORT))
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 255)
status = sock.setsockopt(socket.IPPROTO_IP,socket.IP_ADD_MEMBERSHIP,socket.inet_aton(MCAST_ADDR) + socket.inet_aton(ANY))
sock.setblocking(0)
ts = time.time()
messageParser = apiMessageParser()

#Start the queue monitor so that it can begin detecting tasks placed in the queue
queueMonitor = Thread(target = message_queue_monitor)
queueMonitor.start()

#Continually checks for recieved api messages and if one is found it is added to the back of the queue
while(True):
	try:
		msg, addr = sock.recvfrom(1024)
	except socket.error, e:
		pass
	else:
		if(msg=="quit"):
			print '\033[1;31mShutting down server\033[1;m'
			sys.exit(0)
		else:
			queue.append(msg)