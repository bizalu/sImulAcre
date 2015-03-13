# -*- coding: utf8 -*-
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtNetwork import *
import sys, pickle
from netObject import *
from sense import *

SIZEOF_UINT16 = 2

class HomeWidget(QWidget):

    startClickedS = pyqtSignal()

    def __init__(self, parent=None):
        super(HomeWidget, self).__init__(parent)
        
        self.setupUi()
        self.setupConnect()      


    #@brief design the UX
    def setupUi(self):
      
        logo = QLabel()
        logo.setPixmap(QPixmap("images/logo.png"))
        logo.setFixedSize(210,240)
        logo.setScaledContents(True)
              
        text = QLabel("<p>sImulAcre is a simulation of humain brain ... in fact, it's more a 'simulacre' or a fake of humain brain.</p>")     

        self.start = QPushButton("Start a new conversation", self)
        self.start.setStyleSheet("color:white; font-size:20px; border:0; background-color: #1a7c88; width: 250px; height:40px;border-radius: 10px;")
 
 
        self.logoLayout = QHBoxLayout()
        self.logoLayout.addWidget(logo)
        self.logoLayout.setAlignment(Qt.AlignCenter) 
        
        self.descriptionLayout = QHBoxLayout()
        self.descriptionLayout.addWidget(text)
        self.descriptionLayout.setAlignment(Qt.AlignCenter) 
        
        self.buttonLayout = QHBoxLayout()
        self.buttonLayout.addWidget(self.start)  
        self.buttonLayout.setAlignment(Qt.AlignCenter)      

        principalLayout = QVBoxLayout(self)
        principalLayout.addLayout(self.logoLayout)
        principalLayout.addLayout(self.descriptionLayout)
        principalLayout.addLayout(self.buttonLayout)
        self.setLayout(principalLayout)


    #@brief create connection between SIGNAL/SLOTS
    def setupConnect(self):
        self.start.clicked.connect(self.startClicked)
           
        
    def startClicked(self):
        self.startClickedS.emit()
