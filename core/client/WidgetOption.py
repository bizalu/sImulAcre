# -*- coding: utf8 -*-
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys, imp


#---------------- Widget class --------------------------------------------
#--------------------------------------------------------------------------
class OptionWidget(QWidget):

    finished = pyqtSignal(object)

    def __init__(self, parent=None):
        super(OptionWidget, self).__init__(parent)
        
        self.setupUI()
        self.setupConnect()
        
        self.option = Option()
        self.setClientConfiguration()


#---------------- Qt Graphic/Connect construction --------------------------------------------

    #@brief  create the UX of this widget
    def setupUI(self):

        #Option Layout
        self.connectivity = QLabel("<b>Server connectivity configuration :</b>")       
        self.addressLine = QLineEdit(self)
        self.portLine = QLineEdit(self)

        self.configuration = QLabel("<b>sImulAcre configuration :</b>")
        
        self.langBox = QComboBox()  
        self.voiceBox = QComboBox()         
        self.earBox = QComboBox()
        self.brainBox = QComboBox()

        self.optionLayout = QFormLayout()
        self.optionLayout.addRow(self.connectivity)
        self.optionLayout.addRow("IP address :", self.addressLine)
        self.optionLayout.addRow("Port :", self.portLine)
        self.optionLayout.addRow(" ", None)      
        self.optionLayout.addRow(self.configuration)
        self.optionLayout.addRow("Language :", self.langBox)
        self.optionLayout.addRow("Text to speech module (voice) :", self.voiceBox)
        self.optionLayout.addRow("Speech to text module (ear) :", self.earBox)
        self.optionLayout.addRow("Intelligency module (brain) :", self.brainBox)

        #Bouton Layout
        self.apply = QPushButton("Apply", self)
        self.apply.setStyleSheet("color:white; font-size:20px; border:0; background-color: #1a7c88; width:125px; height:40px; border-radius: 10px;")
        self.cancel = QPushButton("Cancel", self)
        self.cancel.setStyleSheet("color:white; font-size:20px; border:0; background-color: #1a7c88; width:125px; height:40px; border-radius: 10px;")      

        self.buttonLayout = QHBoxLayout()
        self.buttonLayout.addWidget(self.apply)
        self.buttonLayout.addWidget(self.cancel)
        self.buttonLayout.setAlignment(Qt.AlignRight)
        
        #Principal Layout
        principalLayout = QVBoxLayout(self)
        principalLayout.addLayout(self.optionLayout)
        principalLayout.addLayout(self.buttonLayout)
        self.setLayout(principalLayout)


    #@brief create connection between SIGNAL/SLOTS
    def setupConnect(self):
        self.apply.clicked.connect(self.applyClicked)
        self.cancel.clicked.connect(self.cancelClicked)


#----------------- Option Widget methods ----------------------------------------------------

    def applyClicked(self):
        self.option.setServer(self.addressLine.text(), self.portLine.text())
        self.option.setLang(self.langBox.currentText())
        self.option.setEar(self.earBox.currentText())
        self.option.setVoice(self.voiceBox.currentText())
        self.option.setBrain(self.brainBox.currentText())              
        
        self.finished.emit(self.option)
        
    def cancelClicked(self):
        self.finished.emit(self.option)


#----------------- Option methods ---------------------------------------------------------------

    def setClientConfiguration(self):
        #Get list of possible ear configuration
        #earList [ "name", "file path", "supported language"]
        earList = []
        earDir = QDir("../../senses/ears/")
        for file in earDir.entryList(['*.py'], QDir.Files):
            filePath = earDir.absolutePath() + "/" + file
            object = imp.load_source('info', filePath)
            info = object.info()
            name = info.getModuleName()
            lang = info.getSupportedLanguage()
            earList.append([name, filePath, lang])      


        #Get list of possible voice configuration
        #voiceList [ "name", "file path", "supported language"]
        voiceList = []
        voiceDir = QDir("../../senses/voices/")
        for file in voiceDir.entryList(['*.py'], QDir.Files):
            filePath = voiceDir.absolutePath() + "/" + file
            object = imp.load_source('info', filePath)
            info = object.info()
            name = info.getModuleName()
            lang = info.getSupportedLanguage()
            voiceList.append([name, filePath, lang])   


        
        #Set client Configuration into option object
        self.option.setClientOption(earList, voiceList)
        
        
        #Set UI with configuration information
        serverConf = self.option.getServer()
        address = serverConf[0]
        port = serverConf[1]
        ear = self.option.getEar()
        voice = self.option.getVoice()
        
        earList = self.option.getEarList()
        voiceList = self.option.getVoiceList()
        
        self.addressLine.setText(str(address))
        self.portLine.setText(str(port))
        self.voiceBox.addItems(voiceList)
        self.voiceBox.setCurrentIndex(self.voiceBox.findText(voice))
        self.earBox.addItems(earList)
        self.earBox.setCurrentIndex(self.earBox.findText(ear))


    def setServerConfiguration(self, brainList):
        #Set server Configuration into option object
        self.option.setServerOption(brainList)
        
        #Set UI with configuration information
        lang = self.option.getLang()
        brain = self.option.getBrain()
        langList = self.option.getLangList()
        
        langList = self.option.getLangList()
        brainList = self.option.getBrainList()
        
        self.langBox.addItems(langList)
        self.langBox.setCurrentIndex(self.langBox.findText(lang))
        self.brainBox.addItems(brainList)
        self.brainBox.setCurrentIndex(self.brainBox.findText(brain))
        

#---------------- Option class --------------------------------------------
#--------------------------------------------------------------------------
class Option():

    def __init__(self):
        #Default configuration
        self.port = 1412
        self.address = "127.0.0.1"
        
        self.lang = "French"
        
        self.ear = "Google Chrome"
        self.earFile = "../../senses/ears/google.py"
        self.earLang = "fr"
        
        self.voice = "Google translate"
        self.voiceFile = "../../senses/voices/google.py"
        self.voiceLang = "fr"
        
        self.brain = "Cleverbot"
        self.brainFile = "../../brain/cleverbot.py"
        self.brainLang = "fr"

    def setClientOption(self, earList, voiceList):
        self.earList = earList
        self.voiceList = voiceList

    def setServerOption(self, brainList):
        self.brainList = brainList
        

    def setServer(self, address, port):
        self.address = address
        self.port = port
        
    def getServer(self):
        return [ self.address, self.port ]


    def setLang(self, lang):
        self.lang = lang    

    def getLang(self):
        return self.lang

    #@Brief return the list of language compatible with the three module (ear, voice and brain)
    def getLangList(self):
        langPossible = []
        voiceList = []
        earList = []
        brainList = []
        for name, file, langs in self.voiceList:
            for lang, id in langs:
                voiceList = voiceList + [lang]

        for name, file, langs in self.earList:
            for lang, id in langs:
                earList = earList + [lang]

        for name, file, langs in self.brainList:
            for lang, id in langs:
                brainList = brainList + [lang]
        
        langPossible = set(voiceList) & set(earList) & set(brainList)           
        return langPossible

    #@Brief set the current ear module
    def setEar(self, ear):
        self.ear = ear
        
        for name, file, langs in self.earList:
            if name == ear:
                self.earFile = file
                for lang, id in langs:
                    if lang == self.lang:
                        self.earLang = id

    #@Brief return the name of current ear module
    def getEar(self):
        return self.ear

    #@Brief return the list of ear module compatible with selected language
    def getEarList(self):
        earPossible = []
        for name, file, langs in self.earList:
            for lang, id in langs:
                if self.lang == lang:
                    earPossible = earPossible + [name]
        
        return earPossible


    #@Brief set the current voice module
    def setVoice(self, voice):
        self.voice = voice
        
        for name, file, langs in self.voiceList:
            if name == voice:
                self.voiceFile = file
                for lang, id in langs:
                    if lang == self.lang:
                        self.voiceLang = id
                        
    #@Brief return the name of current voice module              
    def getVoice(self):
        return self.voice 

    #@Brief return the list of voice module compatible with selected language
    def getVoiceList(self):
        voicePossible = []
        for name, file, langs in self.voiceList:
            for lang, id in langs:
                if self.lang == lang:
                    voicePossible = voicePossible + [name]
        
        return voicePossible



    #@Brief set the current brain module
    def setBrain(self, brain):
        self.brain = brain
        
        for name, file, langs in self.brainList:
            if name == brain:
                self.brainFile = file
                for lang, id in langs:
                    if lang == self.lang:
                        self.brainLang = id
                        
    #@Brief return the name of current brain module 
    def getBrain(self):
        return self.brain

    #@Brief return the list of brain module compatible with selected language
    def getBrainList(self):
        brainPossible = []
        for name, file, langs in self.brainList:
            for lang, id in langs:
                if self.lang == lang:
                    brainPossible = brainPossible + [name]
        
        return brainPossible           
