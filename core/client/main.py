#!/usr/bin/python3
# -*- coding: utf8 -*-

import sys, signal
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from Interface import *


def main(args):

    #création de l'application
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    
    app = QApplication(args)
    app.setApplicationName("sImulAcre client v0.2")
    app.setWindowIcon(QIcon("images/logo.png"))
    app.setQuitOnLastWindowClosed(True)

    interface = Interface()
    interface.show()

    sys.exit(app.exec())

if __name__ == "__main__" :
   main(sys.argv)
