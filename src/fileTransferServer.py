from socket import *
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
        self.sock = socket()
        self.sock.bind((self.HOST,self.PORT))
            
    def decode_length(self, l):
        while(l[0]=="0"):
            l = l[1:]
        return int(l)
        
    def awaitConnection(self):
        LENGTH_SIZE = 8
        self.sock.listen(10)
        sockConnection, address = self.sock.accept()
        
        sockConnection.send(str(self.imageCounter))
        
        f = open("images/" + str(self.imageCounter) + "-" + self.filename,'wb')
        length = self.decode_length(sockConnection.recv(LENGTH_SIZE))
        
        while(length):
            rec = sockConnection.recv(min(1024, length))
            f.write(rec)
            length -= len(rec)
            
        f.close()
        
        self.imageCounter += 1
        
        sockConnection.send(b'A')
            
        sockConnection.close()
        
    def setFileName(self, filename):
        self.filename = filename
        
    def quitRequest(self):
        self.quit = True
        self.sock.close()
        