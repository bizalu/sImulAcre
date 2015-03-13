# -*- coding: utf8 -*-

import sys, os

class voice():

    def __init__(self, language):
        self.language = language
        if not os.path.isfile("/usr/share/mbrola/" + language + "/" + language):
            sys.stderr.write("The language " + self.language + " doesn't exist. Check the directory /usr/share/mbrola.")
            sys.exit(1)

    def say(self, message):

        try:
            os.system("espeak -s 130 -v mb/mb-" + self.language + " '" + message.replace("'", " ") + "' | mbrola /usr/share/mbrola/" + self.language + "/" + self.language + " - - | aplay")
        except:
            sys.stderr.write("Mbrola's module return the error code")


    def read(self, file):

        try:
            os.system("espeak -s 130 -v mb/mb-" + self.language + " -f '" + file + "' | mbrola /usr/share/mbrola/" + self.language + "/" + self.language + " - - | aplay")
        except:
            sys.stderr.write("Mbrola's module return the error code")


class info():

    def getModuleName(self):
        return "espeak & mbrola"

    def getSupportedLanguage(self):
        #Supported language of mbrola
        return [["French", "fr1"]]
