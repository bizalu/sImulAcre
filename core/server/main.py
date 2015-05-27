#!/usr/bin/python3
# -*- coding: utf8 -*-

import sys, signal
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from sImulAcreServer import sImulAcreServer


def main(args):
    #création de l'application
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    app = QCoreApplication(args)
    locale = QLocale.system().name()
    app.setApplicationName("sImulAcre server v0.1")

    #Lancement du serveur
    server = sImulAcreServer()
    server.start()

    #Lancement de l'application
    sys.exit(app.exec())
    

if __name__ == "__main__" :
   main(sys.argv)
