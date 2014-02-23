import socket
import select
import sys
from threading import Thread
from Queue import Queue
from API import apiMessageParser

queue = Queue([999])

def message_queue_monitor():
	while(True):
		if(queue.empty()!=True):
			qitem = queue.get()
			reply(qitem[0],str(messageParser.processMessage(qitem[1])))
 
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
    PORT = 5001
     
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # why is this not working?
    server_socket.bind(("0.0.0.0", PORT))
    server_socket.listen(10)
 
    CONNECTION_LIST.append(server_socket)
    
    print "API server started on port " + str(PORT)
    
    messageParser = apiMessageParser()
    
    queueMonitor = Thread(target = message_queue_monitor)
    queueMonitor.start()
 
    while 1:
        try:
        	read_sockets,write_sockets,error_sockets = select.select(CONNECTION_LIST,[],[])
        except:
       		continue
 
        for sock in read_sockets:
            if sock == server_socket:
                sockfd, addr = server_socket.accept()
                CONNECTION_LIST.append(sockfd)
                print "Client (%s, %s) connected" % addr
            else:
                try:
                    data = sock.recv(RECV_BUFFER)
                    if data:
                    	if(data == "quit"):
							print '\033[1;31mShutting down server\033[1;m'
							server_socket.close()
							sys.exit(0)
                    	else:
                    		queue.put((sock,data))
                 
                except:
                    print "Client (%s, %s) is offline" % addr
                    sock.close()
                    CONNECTION_LIST.remove(sock)
                    continue
    server_socket.close()