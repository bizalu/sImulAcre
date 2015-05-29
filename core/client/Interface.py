# -*- coding: utf8 -*-
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from WidgetHome import *
from WidgetTalk import *
from WidgetToolbar import *
from WidgetOption import *
from netObject import *
import sys, pickle, socket



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
        #création du socket
        self.mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #envoi d'une requête de connexion au serveur
        try:
           self.mySocket.connect((address, port))
        except socket.error:
           print("La connexion a échoué.")
           sys.exit()    

        print("Connexion établie avec le serveur.")      
        return True

    #@brief close the socket
    def serverDisconnect(self):
        print("Connexion interrompue.")
        self.mySocket.close()

    #@Brief get the list of Intelligence module supported by the server
    def getServerConfiguration(self):
        request = Request("getConf", "brainList")
        brainList = self.serverRequest(request)
        
        return brainList

    #@Brief get the list of Intelligence module supported by the server
    def setServerConfiguration(self, option):
        request = Request("setConf", [option.brain, option.lang])
        self.serverRequest(request)


    #@brief request the server (exchange of netObject) 
    def serverRequest(self, requestObject):
        serialObject = pickle.dumps(requestObject)
        self.mySocket.send(serialObject)

        replyObject = self.mySocket.recv(1024)            
        netObject = pickle.loads(replyObject)
              
        if netObject.type == "thinkAbout":
            print('server say ' + netObject.answer)
            self.talkWidget.serverSay(netObject.answer)
        
        if netObject.type == "getConf":
            print('server send ' + str(netObject.answer))
            return netObject.answer
