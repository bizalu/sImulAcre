#!/usr/bin/python3                                                                                                                                            
# -*- coding: utf8 -*-


from netObject import *
import sys, pickle, socket



class Client():

    def __init__(self):
        self.address = "127.0.0.1"
        self.port = 1412 
        self.brainName = "sImulAcre"
        self.brainLang = "fr"

        self.serverConnect(self.address, self.port)
        self.openConversation(self.brainName, self.brainLang)

#----------------- Client methods ----------------------------------------------------

    #@brief start a conversation with the server ('start a conversation' buttom in homeWidget)
    def openConversation(self, brainName, brainLang):
        self.setServerConfiguration(brainName, brainLang)
        while True:
            clientSay = input("you> ")
            if(clientSay == ""):
                break
            serverSay = self.getServerAnswer(clientSay)
            print("server> " + serverSay)

        self.closeConversation()


    #@brief close the conversation with the server
    def closeConversation(self):
        self.serverDisconnect()
        sys.exit()




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
    def setServerConfiguration(self, brainName, brainLang):
        request = Request("setConf", [brainName, brainLang])
        self.serverRequest(request)


    def getServerAnswer(self, question):
        request = Request("thinkAbout", question)
        answer = self.serverRequest(request)

        return answer
        

    #@brief request the server (exchange of netObject) 
    def serverRequest(self, requestObject):
        serialObject = pickle.dumps(requestObject)
        self.mySocket.send(serialObject)

        replyObject = self.mySocket.recv(1024)            
        netObject = pickle.loads(replyObject)
              
        return netObject.answer


client = Client() 
