import socket
import sys
import os
import glob
from ConfigParser import SafeConfigParser

class fts():
    PORT = ""
    HOST = ""
    filename = "no_filename"
    quit = False
    imageCounter = 0
    
    def __init__(self):
        parser = SafeConfigParser()
        parser.read("config.ini")
        self.PORT = parser.getint('connection','port') + 1
        self.HOST = parser.get('connection','host')
        files = glob.glob('images/*')
        for f in files:
            os.remove(f)
        
    def awaitConnection(self):
        self.sock = socket.socket()
        self.sock.bind((self.HOST,self.PORT))
        self.sock.listen(10)
        sockConnection, address = self.sock.accept()
        
        sockConnection.send(str(self.imageCounter))
        
        f = open("images/" + str(self.imageCounter) + "-" + self.filename,'wb')
        
        self.imageCounter += 1
        
        l = sockConnection.recv(1024)
        while (l):
                f.write(l)
                l = sockConnection.recv(1024)
        f.close()
            
        sockConnection.close()
        self.sock.close()
        print "Recieved All"
        
    def setFileName(self, filename):
        self.filename = filename
        
    def quitRequest(self):
        self.quit = True
        