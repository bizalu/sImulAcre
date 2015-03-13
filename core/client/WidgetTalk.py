# -*- coding: utf8 -*-
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtNetwork import *
import sys, pickle
from netObject import *
from sense import *

SIZEOF_UINT16 = 2

class TalkWidget(QWidget):

    serverRequestedS = pyqtSignal(object)

    def __init__(self, parent=None):
        super(TalkWidget, self).__init__(parent)
        
        self.listen = False
        self.setupUi()
        self.setupConnect()
  
        
#---------------- Qt Graphic/Connect construction --------------------------------------------
    #@brief design the UX
    def setupUi(self):
        self.lyrics = QTextEdit(self)
        self.lyrics.setStyleSheet("background:transparent; border:0;")
        self.lyrics.setReadOnly(True)

        self.say = QLineEdit(self)
        self.say.setStyleSheet("font-size:20px; height:40px;border:0;")
        
        self.send = QPushButton("Send", self)
        self.send.setStyleSheet("color:white; font-size:20px; border:0; background-color: #1a7c88; width: 250px; height:40px;border-radius: 10px;")
        
        self.micro = QPushButton(QIcon("images/mic-officon.png"), "")
        self.micro.setIconSize(QSize(40,40))
        self.micro.setFixedSize(80, 60)
        self.micro.setStyleSheet("border:0; margin:0;")
        
        self.buttons = QHBoxLayout()
        self.buttons.addWidget(self.say)
        self.buttons.addWidget(self.send)
        self.buttons.addWidget(self.micro)
        
        self.progress = QLabel()
        self.progress.setPixmap(QPixmap("images/progress.png"))
        self.progress.setAlignment(Qt.AlignCenter) 

        self.progress1 = QLabel()
        self.progress1.setPixmap(QPixmap("images/progress-etape1.png"))
        self.progress1.setAlignment(Qt.AlignCenter)
        self.progress1.hide() 
        
        self.progress2 = QLabel()
        self.progress2.setPixmap(QPixmap("images/progress-etape2.png"))
        self.progress2.setAlignment(Qt.AlignCenter)
        self.progress2.hide()  

        self.progress3 = QLabel()
        self.progress3.setPixmap(QPixmap("images/progress-etape3.png"))
        self.progress3.setAlignment(Qt.AlignCenter)
        self.progress3.hide()  

        principalLayout = QVBoxLayout(self)
        principalLayout.addWidget(self.lyrics)
        principalLayout.addLayout(self.buttons)
        principalLayout.addWidget(self.progress)
        principalLayout.addWidget(self.progress1)
        principalLayout.addWidget(self.progress2)
        principalLayout.addWidget(self.progress3)
        self.setLayout(principalLayout)


    #@brief create connection between SIGNAL/SLOTS
    def setupConnect(self):
        self.send.clicked.connect(self.sendClicked)
        self.micro.clicked.connect(self.microClicked)


#----------------- talk methods ----------------------------------------------------

    #@brief start a conversation
    def startConversation(self, option):
        self.sense = Sense(option.voiceFile, option.voiceLang, option.earFile, option.earLang)
    
    #@brief start when we click on send button
    def sendClicked(self, clientText=None):
        self.progress.hide()
        self.progress1.show()
        self.repaint()
        if clientText == False:
            clientText = str(self.say.text())
        self.say.clear()
        self.clientSay(clientText)
        
        self.progress1.hide()
        self.progress2.show()
        self.repaint()
        self.questionServer(clientText)
        
    #@brief start when we click on micro button
    def microClicked(self):
        if self.listen == False:
            self.listen = True
            self.micro.setIcon(QIcon("images/mic-onicon.png"))
            self.listenThread = ListenThread(self)
            self.listenThread.finished.connect(self.listenThread.deleteLater)
            self.listenThread.somebodySayS.connect(self.sendClicked)
            self.listenThread.start()

        else:
            self.listen = False
            self.micro.setIcon(QIcon("images/mic-officon.png"))
            self.listenThread.terminate()
            if not self.listenThread.wait(30000):
                print("Error : Listen thread not terminated properly")


    #@brief write into lyrics what sImulAcre say
    def serverSay(self, toSay):
        self.progress2.hide()
        self.progress3.show()
        self.repaint()
        text = self.lyrics.toHtml()
        text += "<p style=\"color:#FFF; background-color:#252525; width:100%; font-size:20px;margin-bottom:10px;\">"+ toSay +"</p>";
        self.lyrics.setText(text)
        self.lyrics.verticalScrollBar().setValue(self.lyrics.verticalScrollBar().maximum())
        self.repaint()
        self.sense.speak(toSay)
        
        self.progress3.hide()
        self.progress.show()
 

    #@brief write into lyrics what User say
    def clientSay(self, toSay):
        text = self.lyrics.toHtml()
        text += "<p style=\"color:#fff; background-color:#f19b1e; width:100%; font-size:20px;margin-bottom:10px;\">"+ toSay +"</p>"
        self.lyrics.setText(text)
        self.lyrics.verticalScrollBar().setValue(self.lyrics.verticalScrollBar().maximum())    


    def questionServer(self, clientText):    
        #Transform what the client say on request object and request the server for answer
        request = Request("sentence", clientText)
        self.serverRequestedS.emit(request)  





class ListenThread(QThread):

    somebodySayS = pyqtSignal(str)

    def __init__(self, parent):
        super(ListenThread, self).__init__(parent)
        self.parent = parent

    def run(self):
        self.parent.progress.hide()
        self.parent.progress1.show()
        
        while True:
            clientText = self.parent.sense.listen()
            
            if clientText != "":
                print('Listen the message ' + clientText)
                self.somebodySayS.emit(clientText)
                
