# -*- coding: utf8 -*-
import sys, socket, pickle, threading, os
from netObject import *
from brain import *


client = {}

class sImulAcreServer():

    def __init__(self):
        self.port = 1412
        self.address = "127.0.0.1"
    
    def start(self):
        print("=========================================================")
        print("sImulAcre server v0.2")
        print("=========================================================")
        
        # Initialisation du serveur - Mise en place du socket :
        mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            mySocket.bind((self.address, self.port))

        except socket.error:
            print("La liaison du socket à l'adresse choisie a échoué.")
            sys.exit()

        print("Serveur prêt, en attente de requêtes ...")
        mySocket.listen(5)        


        # Attente et prise en charge des connexions demandées par les clients :
        while 1:    
            connexion, adresse = mySocket.accept()

            # Créer un nouvel objet thread pour gérer la connexion :
            th = ThreadClient(connexion)
            th.start()

            # Mémoriser la connexion dans le dictionnaire : 
            it = th.getName()        # identifiant du thread
            client[it] = connexion
            print("Client " + str(it) + " connecté, adresse IP " + str(adresse[0]) + ", port " + str(adresse[1]))



class ThreadClient(threading.Thread):

    def __init__(self, conn):
        threading.Thread.__init__(self)
        self.connexion = conn

        self.brain = ""
        
        #Default configuration
        self.lang = "French"
        
        self.brainName = "Cleverbot"
        self.brainFile = "../../brain/cleverbot.py"
        self.brainLang = "fr"
        
        #Existing possible configuration
        self.brainList = self.getServerConfiguration()
        self.brain = Brain(self.brainFile, self.brainLang) 



    def run(self):
        # Dialogue avec le client :
        nom = self.getName()        # Chaque thread possède un nom

        while 1:
            msgClient = self.connexion.recv(1024)

            if msgClient.upper() == "FIN" or msgClient == "":
                break
            
            if msgClient :
                self.readMessage(msgClient)


        # Fermeture de la connexion :
        self.connexion.close()      # couper la connexion côté serveur
        del client[nom]        # supprimer son entrée dans le dictionnaire
        print("Client " + nom + " déconnecté.")
           
        
    def readMessage(self, msg): 
        netObject = pickle.loads(msg)
            
        if netObject.type == "thinkAbout":
            netObject.answer = self.brain.thinkAbout(netObject.request)
            self.sendMessage(netObject)
        elif netObject.type == "getConf":
            netObject.answer = self.getServerConfiguration()
            self.sendMessage(netObject)
        elif netObject.type == "setConf":
            netObject.answer = self.setServerConfiguration(netObject.request)
            self.sendMessage(netObject)
        else:
            print("Error : unknow type " + netObject.type)     



    def sendMessage(self, msg):
        netObject = pickle.dumps(msg)
        self.connexion.send(netObject)



    #@Brief Get list of possible brain configuration
    def getServerConfiguration(self):
        #brainList [ "name", "file path", "supported language"]
        brainList = []
        for file in os.listdir("../../brain/"):
            if file.endswith(".py"):
                filePath = os.path.abspath("../../brain/" + file)
                object = imp.load_source('info', filePath)
                info = object.info()
                name = info.getModuleName()
                lang = info.getSupportedLanguage()
                brainList.append([name, filePath, lang])
        
        return brainList   

    #@Brief set the current brain module
    def setServerConfiguration(self, brainConf):
        #brainConf [name, lang]
        self.brainName = brainConf[0]
        self.lang = brainConf[1]
        
        for name, file, langs in self.brainList:
            if name == self.brainName:
                self.brainFile = file
                for lang, id in langs:
                    if lang == self.lang:
                        self.brainLang = id
                        
        self.brain = Brain(self.brainFile, self.brainLang)
        
        return "OK"
