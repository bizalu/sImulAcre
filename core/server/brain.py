import json, sys, os, imp, re

class Brain():
    
    def __init__(self, brainFile, brainLang):
        #temporary
        key = ""
        
        #Verification de l'existance des fichiers à importer
        if not os.path.isfile(brainFile):
            sys.stderr.write("The file " + brainFile + " doesn't exist")
            sys.exit(1)


        #Declaration des objets brain
        object = imp.load_source('brain', brainFile)
        self.brain = object.brain(key)


    def thinkAbout(self, message):

        retour = self.brain.think(message)
        return retour

