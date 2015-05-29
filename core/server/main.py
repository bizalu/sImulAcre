#!/usr/bin/python3
# -*- coding: utf8 -*-

import sys, signal
from sImulAcreServer import sImulAcreServer



if __name__ == "__main__" :
    #Lancement du serveur
    server = sImulAcreServer()
    server.start()

