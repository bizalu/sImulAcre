import sys, os, imp, re

class Sense():
    
    def __init__(self, voicefile, voicelang, earsfile, earslang):

        #Verification de l'existance des fichiers à importer
        if not os.path.isfile(voicefile):
            sys.stderr.write("The file " + voicefile + " doesn't exist")
            sys.exit(1)

        if not os.path.isfile(earsfile):
            sys.stderr.write("The file " + earsfile + " doesn't exist")
            sys.exit(1)

        #Declaration des objets voice et ears
        obj = imp.load_source('voice', voicefile)
        self.voice = obj.voice(voicelang)

        obj = imp.load_source('ears', earsfile)
        self.ears = obj.ears(earslang)      


    def listen(self):
        message = self.ears.listen()        
        return message
 

    def speak(self, message):
        self.voice.say(message)

