# -*- coding: utf8 -*-
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from WidgetHome import *
from WidgetTalk import *
from WidgetToolbar import *
from WidgetOption import *
from netObject import *
import sys, pickle



class Interface(QDialog):

    def __init__(self):
        super(Interface, self).__init__()
        
        self.setupUi()
        self.setupConnexions()
        
        self.goToHomeMode()
        self.startServerConnection()

#---------------- Qt Graphic/Connect construction --------------------------------------------

    #@brief  create the UX
    def setupUi(self):

        self.setWindowIcon(QIcon("images/logo.png"))
        self.setWindowTitle("sImulAcre v0.1")
        self.setWindowIconText("sImulAcre v0.1")
        
        self.background = QLabel(self)
        self.background.setPixmap(QPixmap('images/background.png'))

        self.homeWidget = HomeWidget(self)
        self.homeWidget.hide()

        self.optionWidget = OptionWidget(self)
        self.optionWidget.hide()
        
        self.talkWidget = TalkWidget(self)
        self.talkWidget.hide()

        self.toolbarLeft = Toolbar(self)
        self.toolbarLeft.setMaximumWidth(80)

        self.layoutPrincipal = QHBoxLayout()
        self.layoutPrincipal.addWidget(self.toolbarLeft)
        self.layoutPrincipal.addWidget(self.homeWidget)
        self.layoutPrincipal.addWidget(self.optionWidget)
        self.layoutPrincipal.addWidget(self.talkWidget)
        self.setLayout(self.layoutPrincipal)


    #@brief show WidgetTalk
    def goToHomeMode(self):       
        self.optionWidget.hide()
        self.talkWidget.hide()
        self.homeWidget.hide()
        
        self.homeWidget.show()      
        self.resizeEvent(None)
        

    #@brief show WidgetTalk
    def goToTalkMode(self):        
        self.optionWidget.hide()
        self.talkWidget.hide()
        self.homeWidget.hide()

        self.talkWidget.show()     
        self.resizeEvent(None)


    #@brief show WidgetOption
    def goToOptionMode(self):      
        self.talkWidget.hide()
        self.optionWidget.hide()
        self.homeWidget.hide()

        self.optionWidget.show()
        self.resizeEvent(None)
        
        
    #@brief operate QObject connect
    def setupConnexions(self):
        self.toolbarLeft.homeModeClickedS.connect(self.goToHomeMode)
        self.toolbarLeft.talkModeClickedS.connect(self.goToTalkMode)
        self.toolbarLeft.optionModeClickedS.connect(self.goToOptionMode)
        self.optionWidget.finished.connect(self.closeConversation)
        self.homeWidget.startClickedS.connect(self.openConversation)
        self.talkWidget.serverRequestedS.connect(self.serverRequest)


    #@brief resize the UI
    def resizeEvent(self, QResizeEvent):
        self.background.resize(self.width(), self.height())
        self.background.setScaledContents(True)
        self.toolbarLeft.resize(80, self.height())
        self.toolbarLeft.move(0,0)



#----------------- Client methods ----------------------------------------------------

    #@brief start server's connection and set it's configuration into optionWidget
    def startServerConnection(self):
        if self.serverConnect(self.optionWidget.option.address, self.optionWidget.option.port):
            brainList = self.getServerConfiguration()
            self.optionWidget.setServerConfiguration(brainList)


    #@brief start a conversation with the server ('start a conversation' buttom in homeWidget)
    def openConversation(self):
        self.toolbarLeft.enableTalkMode(True)
        self.setServerConfiguration(self.optionWidget.option)
        self.talkWidget.startConversation(self.optionWidget.option)
        self.goToTalkMode()


    #@brief close the conversation with the server
    def closeConversation(self):
        self.toolbarLeft.enableTalkMode(False)
        self.goToHomeMode()




#--------------- Client to server methods ---------------------------------------------

    #@brief connect to the server with socket /based on option object/
    def serverConnect(self, address, port):
        self.socket = QTcpSocket()
        
        self.socket.connectToHost(str(address), int(port))
        
        if not self.socket.waitForConnected(5000):
            print("The server " + str(address) + ":" + str(port) + " is down. Please start the server first.")
            connected = False
        else:
            connected = True
        
        return connected

    #@brief close the socket
    def serverDisconnect(self):
        self.socket.disconnectFromHost()

    #@Brief get the list of Intelligence module supported by the server
    def getServerConfiguration(self):
        request = Request("get", "brainList")
        brainList = self.serverRequest(request)
        
        return brainList

    #@Brief get the list of Intelligence module supported by the server
    def setServerConfiguration(self, option):
        request = Request("set", [option.brain, option.lang])
        self.serverRequest(request)


    #@brief request the server (exchange of netObject) 
    def serverRequest(self, requestObject):
        #Serialise the object and transform it on socket
        print('Serialise Object')
        serialObject = pickle.dumps(requestObject)
        
        netObject = QByteArray()
        askStream = QDataStream(netObject, QIODevice.WriteOnly)
        askStream.setVersion(QDataStream.Qt_4_2)

        askStream.writeUInt16(0)
        askStream.writeBytes(serialObject)
        askStream.device().seek(0)
        askStream.writeUInt16(netObject.size() - SIZEOF_UINT16)

        #Send the socket
        print('send object')
        self.socket.write(netObject)
        if not self.socket.waitForBytesWritten():
            print("Error : this sentence can't be transmit to the server")    

        #Receive the socket
        print('receive object')
        replyStream = QDataStream(self.socket)
        replyStream.setVersion(QDataStream.Qt_4_2)
        
        nextBlockSize = 0
        if (self.socket.waitForReadyRead(-1) and self.socket.bytesAvailable() >= SIZEOF_UINT16):
            nextBlockSize = replyStream.readUInt16()
        else:
            print("Cannot read client request")
            return
            
        if self.socket.bytesAvailable() < nextBlockSize:
            if (not self.socket.waitForReadyRead(-1) or self.socket.bytesAvailable() < nextBlockSize):
                print("Cannot read client data")
                return
        
        #Unserialise the object
        print('unserialise object')
        data = replyStream.readBytes()            
        netObject = pickle.loads(data)
        
        if netObject.type == "sentence":
            print('server say ' + netObject.answer)
            self.talkWidget.serverSay(netObject.answer)
        
        if netObject.type == "get":
            print('server send ' + str(netObject.answer))
            return netObject.answer
