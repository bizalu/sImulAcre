# -*- coding: utf8 -*-
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtNetwork import *
import sys, pickle
from netObject import *
from brain import *


SIZEOF_UINT16 = 2 

class sImulAcreServer(QTcpServer):

    def __init__(self, parent=None):
        super(sImulAcreServer, self).__init__(parent)
        self.port = 1412
    
    def start(self):
        print("=========================================================")
        print("sImulAcre server v0.1 ")
        print("=========================================================")
        
        if (not self.listen(QHostAddress.Any, self.port)):
            print("Server can't run")
            print("Exit")
            sys.exit(1)
        else:
            print("Server is running\n")
        
    
    #@brief Create a thread by connection 
    def incomingConnection(self, socketDescriptor):
        print("New connection to sImulAcre server")
        thread = Thread(socketDescriptor, self)
        thread.finished.connect(thread.deleteLater)
        thread.start()      

class Thread(QThread):

    def __init__(self, socketDescriptor, parent):
        super(Thread, self).__init__(parent)
        self.socketDescriptor = socketDescriptor
        self.brain = ""
        
        #Default configuration
        self.lang = "French"
        
        self.brainName = "Cleverbot"
        self.brainFile = "../../brain/cleveverbot.py"
        self.brainLang = "fr"
        
        #Existing possible configuration
        self.brainList = self.getServerConfiguration()


    #@brief Get the data information from the received socket and call appropriate methods
    #Call by the Thread.start() method
    def run(self):
        self.socket = QTcpSocket()
        self.socket.setSocketDescriptor(self.socketDescriptor)
        
        while self.socket.state() == QAbstractSocket.ConnectedState:
            nextBlockSize = 0
            stream = QDataStream(self.socket)
            stream.setVersion(QDataStream.Qt_4_2)
            
            if (self.socket.waitForReadyRead(-1) and self.socket.bytesAvailable() >= SIZEOF_UINT16):
                nextBlockSize = stream.readUInt16()
            else:
                print("Cannot read client request")
                return
                
            if self.socket.bytesAvailable() < nextBlockSize:
                if (not self.socket.waitForReadyRead(-1) or self.socket.bytesAvailable() < nextBlockSize):
                    print("Cannot read client data")
                    return
            
            data = stream.readBytes()            
            netObject = pickle.loads(data)
            
            if netObject.type == "sentence":
                netObject.answer = self.brain.thinkAbout(netObject.request)
                self.sendReply(netObject)
            elif netObject.type == "get":
                netObject.answer = self.brainList
                self.sendReply(netObject)
            elif netObject.type == "set":
                netObject.answer = self.setServerConfiguration(netObject.request)
                self.sendReply(netObject)
            else:
                print("Error : unknow type " + netObject.type)     


    #@Brief Get list of possible brain configuration
    def getServerConfiguration(self):
        #brainList [ "name", "file path", "supported language"]
        brainList = []
        brainDir = QDir("../../brain/")
        for file in brainDir.entryList(['*.py'], QDir.Files):
            filePath = brainDir.absolutePath() + "/" + file
            object = imp.load_source('info', filePath)
            info = object.info()
            name = info.getModuleName()
            lang = info.getSupportedLanguage()
            brainList.append([name, filePath, lang])
        
        return brainList   

    #@Brief set the current brain module
    def setServerConfiguration(self, brainConf):
        #brainConf [name, lang]
        self.BrainName = brainConf[0]
        self.lang = brainConf[1]
        
        for name, file, langs in self.brainList:
            if name == self.brainName:
                self.brainFile = file
                for lang, id in langs:
                    if lang == self.lang:
                        self.brainLang = id
                        
        self.brain = Brain(self.brainFile, self.brainLang)
        
        return "OK"
        
        

    def sendReply(self, replyObject):
    
        serialObject = pickle.dumps(replyObject)
        
        netObject = QByteArray()
        stream = QDataStream(netObject, QIODevice.WriteOnly)
        stream.setVersion(QDataStream.Qt_4_2)

        stream.writeUInt16(0)
        stream.writeBytes(serialObject)
        stream.device().seek(0)
        stream.writeUInt16(netObject.size() - SIZEOF_UINT16)

        self.socket.write(netObject)
        if not self.socket.waitForBytesWritten():
            print("Error : this sentence can't be transmit to the client")   

            
