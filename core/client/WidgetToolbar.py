# -*- coding: utf8 -*-
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from WidgetTalk import *
import sys

class Toolbar(QWidget):

    talkModeClickedS = pyqtSignal()
    optionModeClickedS = pyqtSignal()
    homeModeClickedS = pyqtSignal()

    def __init__(self, parent=None):
        super(Toolbar, self).__init__(parent)
        self.setupUi()
        self.setupConnect()


    #@brief design the UX
    def setupUi(self):

        self.setStyleSheet("QPushButton { border:0; margin:0;} QPushButton::hover { background-color: #f19b1e; }")
        self.background = QLabel(self)
        self.background.setStyleSheet("background-color: #252525;")
        
        logo = QLabel()
        logo.setPixmap(QPixmap("images/logo.png"))
        logo.setFixedSize(80,110)
        logo.setScaledContents(True)

        self.homeMode = QPushButton(QIcon("images/homeicon.png"), "")
        self.homeMode.setIconSize(QSize(40,40))
        self.homeMode.setFixedSize(80, 60)
        
        self.talkMode = QPushButton(QIcon("images/talkicon.png"), "")
        self.talkMode.setIconSize(QSize(40,40))
        self.talkMode.setFixedSize(80, 60)
        self.talkMode.setDisabled(True)
        
        self.optionMode = QPushButton(QIcon("images/optionicon.png"), "")
        self.optionMode.setIconSize(QSize(40,40))
        self.optionMode.setFixedSize(80, 60)

        principalLayout = QVBoxLayout(self)
        principalLayout.addSpacing(20)
        principalLayout.addWidget(logo)
        principalLayout.addStretch(1)
        principalLayout.addWidget(self.homeMode)
        principalLayout.addWidget(self.talkMode)
        principalLayout.addWidget(self.optionMode)
        principalLayout.setAlignment(Qt.AlignCenter)
        principalLayout.setContentsMargins(0,0,0,0)
                
        self.setLayout(principalLayout)


    #@brief create connection between SIGNAL/SLOTS
    def setupConnect(self):
        self.homeMode.clicked.connect(self.homeModeClicked)
        self.talkMode.clicked.connect(self.talkModeClicked)
        self.optionMode.clicked.connect(self.optionModeClicked)

    #@brief start when we click on talk button
    def homeModeClicked(self):
        self.homeModeClickedS.emit()
        self.setFocus()

    #@brief start when we click on talk button
    def talkModeClicked(self):
        self.talkModeClickedS.emit()
        self.setFocus()


    #@brief start when we click on talk button
    def optionModeClicked(self):
        self.optionModeClickedS.emit()
        self.setFocus()


    #@brief start when we resize the window
    def resizeEvent(self, qResizeEvent):
        self.background.resize(self.width(), self.height())
        self.background.setScaledContents(True)

    #@brief start when we click on "Start a conversation" button from WidgetHome
    def enableTalkMode(self, state):
        self.talkMode.setEnabled(state)
