import socket
import sys
from ConfigParser import SafeConfigParser

class fts():
    PORT = ""
    HOST = ""
    filename = "no_filename"
    quit = False
    
    def __init__(self):
        parser = SafeConfigParser()
        parser.read("config.ini")
        self.PORT = parser.getint('connection','port') + 1
        self.HOST = parser.get('connection','host')
        
        self.sock = socket.socket()
        self.sock.bind((self.HOST,self.PORT))
        self.sock.listen(10)
        
    def awaitConnection(self):
        sockConnection, address = self.sock.accept()
        
        f = open("images/" + self.filename,'wb')
        
        l = sockConnection.recv(1024)
        while (l):
                f.write(l)
                l = sockConnection.recv(1024)
        f.close()
            
        sockConnection.close()
        self.sock.close()
        
    def setFileName(self, filename):
        self.filename = filename
        
    def quitRequest(self):
        self.quit = True